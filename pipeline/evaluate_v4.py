"""Frozen controlled-passage evaluation; synthetic copies live only in parallax_eval."""
import os,json,re,gzip,base64,concurrent.futures,random,datetime
from collections import Counter
import numpy as np
from .common import ROOT,WORK,db,digest,now
from .extract import split_claims
from .sources import chunks
from .embeddings import encoder
from .prompts import VERSION,RECALL_PROMPT,PRECISION_PROMPT
from .check import build_groups,process_batch

DATE_IDS=['fcca9bf2bbc3d59be8b7a0c489575d40','92cc5ae8086cc2f5d461a0ee9c1d10ea','d0796c8b633cbce49e30e46443cc6255','d7d836bdbea0ae40b50bfdf62256502e','7418954ca982f4166fe639107026e752','21e51447696dddd666d8a6e43acc4bd1','ffa7b397b69fb6188675b387364b3e20','364a675a105f79f1d045a39815cf5210']
NUMBER_IDS=['63de97733b940ef743971c78df3d5c49','baddac456aeaf5ed7c786a1d9201248f','4c341d7dbd7b20b349fe8fbd3638ea2a','b6bd528ad3303e9247cdcfba2ec804af','ef3fa575b130db2e957da32a58ab55ad','2456d89e534ade8b2d4562df7758b5c6','b69b726fd64ceb31ab18100afdccfdb2','0311a2b6a5b18e82fc0e2d6704dfb509']

def cases():
 labels=json.loads((ROOT/'eval/parallax/control-labels.json').read_text());ids=labels['intact_clean_ids']+list(labels['supported_excerpts']);drops=list(labels['counterparts']);used=set(drops+DATE_IDS+NUMBER_IDS);remaining=[i for i in ids if i not in used];assert len(remaining)==16
 kinds={**dict.fromkeys(drops,'dropped_sentence'),**dict.fromkeys(DATE_IDS,'wrong_date'),**dict.fromkeys(NUMBER_IDS,'wrong_number'),**dict.fromkeys(remaining[:8],'loaded_wording'),**dict.fromkeys(remaining[8:],'unsupported_claim')}
 out=[]
 for cid in ids:
  original=json.loads((WORK/f'eval/{cid}.json').read_text());base=labels['supported_excerpts'].get(cid,original['claim']['text']);assert base in original['claim']['text'];kind=kinds[cid]
  for planted in [False,True]:
   text=base;changed=[];counterpart=None
   if planted:
    if kind=='wrong_date':
     years=re.findall(r'\b(?:1\d{3}|20\d{2})\b',text);assert years,cid
     # Shift a whole stated interval consistently, so overlapping subranges are not ambiguous controls.
     text=re.sub(r'\b(?:1\d{3}|20\d{2})\b',lambda m:str(int(m.group())+10),text);changed=[str(int(y)+10) for y in years]
    elif kind=='wrong_number':
     matches=list(re.finditer(r'\b\d[\d,]*(?:\.\d+)?\b',text));assert matches,cid;m=next((m for m in matches if not (len(m.group())==4 and 1000<=float(m.group().replace(',',''))<=2029)),matches[0]);new=str(int(float(m.group().replace(',','')))+17);text=text[:m.start()]+new+text[m.end():];changed=[new]
    elif kind=='loaded_wording':text='The utterly magnificent and unquestionably brilliant achievement was this: '+base;changed=['utterly magnificent','unquestionably brilliant']
    elif kind=='unsupported_claim':text=base+' The cited source attributes this to funding from the Swedish Academy.';changed=['funding from the Swedish Academy']
    elif kind=='dropped_sentence':text='';counterpart=labels['counterparts'][cid];changed=[counterpart['text']]
   ident=digest(['heldout-v4',cid,planted])[:32]
   out.append({'id':ident,'qid':'E'+ident[:22],'original_id':cid,'kind':kind,'planted':planted,'text':text,'changed':changed,'counterpart':counterpart,'article':original['article'],'source':original['source'],'construction':'intact claim' if cid in labels['intact_clean_ids'] else 'exact supported excerpt'})
 random.Random(2026111504).shuffle(out);return out

def setup(allcases):
 os.environ['PARALLAX_DB_NAME']='parallax_eval';from server.db import connect
 con=connect(None)
 with con.cursor() as cur:
  for stmt in (ROOT/'pipeline/schema.sql').read_text().replace('parallax','parallax_eval').split(';'):
   if stmt.strip():cur.execute(stmt)
 con.close();c=db();cur=c.cursor();model=encoder();loaded=set();casegroups={}
 for case in allcases:
  qid=case['qid'];url=case['source']['url'];sid=case['source']['id'];source=case['source']
  if sid not in loaded:
   cur.execute('REPLACE INTO cited_source VALUES (%s,%s,%s,%s,%s,%s,UTC_TIMESTAMP(),%s,%s)',(sid,url,source['title'],'Read',source.get('archive_url'),source['text'],digest(source['text']),json.dumps({'evaluation_only':True})))
   texts=chunks(source['text']);vs=model.encode(texts,batch_size=64,normalize_embeddings=True,show_progress_bar=False)
   cur.executemany('REPLACE INTO source_chunk VALUES (%s,%s,%s,%s,%s)',[(digest([sid,i,t])[:32],sid,i,t,np.asarray(v,dtype='<f4').tobytes()) for i,(t,v) in enumerate(zip(texts,vs))]);loaded.add(sid)
  versions={'en':case['text']}
  if case['counterpart']:versions[case['counterpart']['lang']]=case['counterpart']['text']
  for lang,text in versions.items():
   # These are explicitly controlled article-passage copies, never full-article accuracy claims.
   wt=text+(f'<ref>{{{{cite web|url={url}|title=Source}}}}</ref>' if text and lang=='en' else '')
   a={'qid':qid,'lang':lang,'page_id':1,'rev_id':case['article']['rev_id'],'title':case['article']['title'],'wikitext':wt}
   cur.execute('REPLACE INTO article VALUES (%s,%s,1,%s,%s,UTC_TIMESTAMP(),%s,%s)',(qid,lang,a['rev_id'],a['title'],wt,'Controlled held-out passage copy'))
   claims=split_claims(a)
   if claims:
    vs=model.encode([cl['text'] for cl in claims],batch_size=64,normalize_embeddings=True,show_progress_bar=False)
    for cl,v in zip(claims,vs):
     cur.execute('REPLACE INTO claim VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cl['id'],qid,lang,cl['rev_id'],cl['ordinal'],cl['section'],cl['text'],json.dumps(cl['citations']),None,np.asarray(v,dtype='<f4').tobytes()))
     if lang=='en':cur.execute('REPLACE INTO claim_source VALUES (%s,%s)',(cl['id'],sid))
  groups=build_groups(qid)
  # Test the modified assertion rather than counting unrelated flags on the unchanged clause.
  if case['planted'] and case['kind']=='unsupported_claim':groups=[g for g in groups if any('funding from the Swedish Academy' in r['text'] and r['id']==g['anchor_id'] for rs in g['candidates'].values() for r in rs)]
  casegroups[case['id']]=groups
 c.close();return casegroups

def main():
 allcases=cases();directory=WORK/'heldout-v4';directory.mkdir(exist_ok=True)
 frozen=directory/'FROZEN.json'
 manifest={'frozen_at':now(),'prompt_version':VERSION,'recall_sha256':digest(RECALL_PROMPT),'precision_sha256':digest(PRECISION_PROMPT),'case_sha256':digest(allcases),'errors':40,'controls':40,'controls_intact':17,'controls_supported_excerpts':23,'scope':'Controlled copies of real Wikipedia passages, not full-article population accuracy. Eight dropped-sentence cases use original fi/sv counterparts and controlled English passage copies. Real source documents and native MariaDB retrieval are used.','case_metadata':[{k:v for k,v in x.items() if k!='source'}|{'source_url':x['source']['url'],'source_sha256':digest(x['source']['text'])} for x in allcases]}
 if frozen.exists():
  old=json.loads(frozen.read_text());assert old['case_sha256']==manifest['case_sha256'];manifest=old
 else:frozen.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 (ROOT/'eval/parallax/FROZEN.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));groupmap=setup(allcases)
 def work(case):
  path=directory/f'{case["id"]}.json'
  if path.exists():return json.loads(path.read_text())
  try:
   flags=[]
   for group in groupmap[case['id']]:flags+=process_batch([group])
   matched=[]
   for f in flags:
    if case['kind']=='dropped_sentence':hit=f['verdict']=='Missing in English'
    else:hit=any(a in m or m in a for a in case['changed'] for ms in f.get('marks',{}).values() for m in ms)
    if hit:matched.append(f['id'])
   result={'id':case['id'],'kind':case['kind'],'planted':case['planted'],'flags':flags,'caught':bool(matched) if case['planted'] else False,'false_flag':bool(flags) if not case['planted'] else False,'complete':True,'at':now()}
  except Exception as e:result={'id':case['id'],'kind':case['kind'],'planted':case['planted'],'complete':False,'error_type':type(e).__name__,'at':now()}
  path.write_text(json.dumps(result,ensure_ascii=False,indent=2));return result
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(work,allcases))
 aggregate={'measured_at':now(),'prompt_version':VERSION,'scope':manifest['scope'],'errors':40,'controls':40,'caught':sum(r.get('caught',False) for r in results),'false_flags':sum(r.get('false_flag',False) for r in results),'complete':all(r['complete'] for r in results),'checks':{}}
 mapping={'wrong_date':'fact','wrong_number':'fact','dropped_sentence':'lang','loaded_wording':'tone','unsupported_claim':'src'}
 for check in ['src','fact','lang','tone']:
  rs=[r for r in results if mapping[r['kind']]==check];aggregate['checks'][check]={'errors':sum(r['planted'] for r in rs),'controls':sum(not r['planted'] for r in rs),'caught':sum(r.get('caught',False) for r in rs),'false_flags':sum(r.get('false_flag',False) for r in rs)}
 aggregate['by_error_type']={kind:{'caught':sum(r.get('caught',False) for r in results if r['kind']==kind),'errors':8} for kind in mapping};aggregate['classification_note']='Rows group cases by planted error type; a source check can catch a wrong fact. False-flag controls are source-supported passages, mostly single-language; this does not measure multilingual clean-pair false-positive rate.'
 (directory/'RESULTS.json').write_text(json.dumps(aggregate,indent=2));(ROOT/'eval/parallax/RESULTS.json').write_text(json.dumps(aggregate,indent=2))
 if aggregate['complete']:
  c=db('parallax');cur=c.cursor();cur.execute('REPLACE INTO evaluation VALUES (%s,%s,UTC_TIMESTAMP())',('planted',json.dumps(aggregate)));c.close()
 print(json.dumps(aggregate),flush=True)
if __name__=='__main__':main()
