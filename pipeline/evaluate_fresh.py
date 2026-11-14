"""Fresh article-family held-out measurement after the empty-version regression fix."""
import json,re,random,concurrent.futures
from .common import ROOT,WORK,db,digest,now
from .prompts import VERSION,RECALL_PROMPT,PRECISION_PROMPT
from .check import process_batch
from .evaluate_v4 import setup

def cases():
 labels=json.loads((ROOT/'eval/parallax/FRESH-CONTROLS.json').read_text());out=[]
 for row in labels['controls']:
  original=json.loads((WORK/f'eval-fresh/{row["original_id"]}.json').read_text());base=row['clean_text'];kind=row['kind']
  for planted in [False,True]:
   text=base;changed=[];counterpart=None
   if planted:
    if kind=='wrong_date':
     match=re.search(r'\b(?:1\d{3}|20\d{2})\b',text);assert match
     old=match.group();new=str(int(old)+1);text=text[:match.start()]+new+text[match.end():];changed=[new]
    elif kind=='wrong_number':
     matches=[m for m in re.finditer(r'\b\d[\d,]*\b',text) if not 1800<=int(m.group().replace(',',''))<=2100]
     if row['id']=='4aafef868d5dd19175a760e70eb0fbaf':matches=[m for m in matches if m.group()=='16']
     assert matches;match=matches[0];old=int(match.group().replace(',',''));new=str(old+7);text=text[:match.start()]+new+text[match.end():];changed=[new]
    elif kind=='loaded_wording':text='The utterly magnificent and unquestionably brilliant achievement was this: '+base;changed=['utterly magnificent','unquestionably brilliant']
    elif kind=='unsupported_claim':text=base+' The cited source attributes this to funding from the Swedish Academy.';changed=['funding from the Swedish Academy']
    else:text='';counterpart=row['counterpart'];changed=[counterpart['text']]
   ident=digest(['fresh-heldout-v4',row['id'],planted])[:32]
   out.append({'id':ident,'qid':'F'+ident[:22],'original_id':row['id'],'kind':kind,'planted':planted,'text':text,'changed':changed,'counterpart':counterpart,'article':original['article'],'source':original['source'],'construction':row['construction']})
 random.Random(2026111507).shuffle(out);return out

def main():
 allcases=cases();directory=WORK/'heldout-fresh-v4';directory.mkdir(exist_ok=True)
 manifest={'frozen_at':now(),'prompt_version':VERSION,'recall_sha256':digest(RECALL_PROMPT),'precision_sha256':digest(PRECISION_PROMPT),'pipeline_sha256':digest((ROOT/'pipeline/check.py').read_text()),'case_sha256':digest(allcases),'errors':40,'controls':40,'scope':'Fresh article families disjoint from the first evaluated set. Controlled passage copies with article titles, actual sources and eight original fi/sv counterparts; 12 intact controls and 28 exact supported excerpts. This is not full-article population accuracy.','case_metadata':[{k:v for k,v in x.items() if k!='source'}|{'source_url':x['source']['url'],'source_sha256':digest(x['source']['text'])} for x in allcases]}
 path=ROOT/'eval/parallax/FRESH-FROZEN.json'
 if path.exists():
  old=json.loads(path.read_text());assert old['case_sha256']==manifest['case_sha256'];assert old['pipeline_sha256']==manifest['pipeline_sha256'];manifest=old
 else:path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 groupmap=setup(allcases,database='parallax_eval_fresh',include_title=True)
 def work(case):
  path=directory/f'{case["id"]}.json'
  if path.exists():return json.loads(path.read_text())
  try:
   flags=[]
   for group in groupmap[case['id']]:flags+=process_batch([group])
   matched=[f['id'] for f in flags if f['verdict']=='Missing in English'] if case['kind']=='dropped_sentence' else [f['id'] for f in flags if any(a in m or m in a for a in case['changed'] for ms in f.get('marks',{}).values() for m in ms)]
   result={'id':case['id'],'kind':case['kind'],'planted':case['planted'],'flags':flags,'caught':bool(matched) if case['planted'] else False,'false_flag':bool(flags) if not case['planted'] else False,'complete':True,'at':now()}
  except Exception as e:result={'id':case['id'],'kind':case['kind'],'planted':case['planted'],'complete':False,'error_type':type(e).__name__,'at':now()}
  path.write_text(json.dumps(result,ensure_ascii=False,indent=2));return result
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(work,allcases))
 mapping={'wrong_date':'fact','wrong_number':'fact','dropped_sentence':'lang','loaded_wording':'tone','unsupported_claim':'src'}
 aggregate={'measured_at':now(),'prompt_version':VERSION,'scope':manifest['scope'],'errors':40,'controls':40,'caught':sum(r.get('caught',False) for r in results),'false_flags':sum(r.get('false_flag',False) for r in results),'complete':all(r['complete'] for r in results),'checks':{}}
 for check in ['src','fact','lang','tone']:
  rs=[r for r in results if mapping[r['kind']]==check];aggregate['checks'][check]={'errors':sum(r['planted'] for r in rs),'controls':sum(not r['planted'] for r in rs),'caught':sum(r.get('caught',False) for r in rs),'false_flags':sum(r.get('false_flag',False) for r in rs)}
 aggregate['by_error_type']={kind:{'caught':sum(r.get('caught',False) for r in results if r['kind']==kind),'errors':8} for kind in mapping}
 aggregate['classification_note']='Planted categories determine the row; the source check may catch a wrong fact. Controls are source-supported passages, mostly single-language; this does not measure clean multilingual article-pair false-positive rates.'
 (ROOT/'eval/parallax/FRESH-RESULTS.json').write_text(json.dumps(aggregate,indent=2))
 if aggregate['complete']:
  c=db('parallax');cur=c.cursor();cur.execute('REPLACE INTO evaluation VALUES (%s,%s,UTC_TIMESTAMP())',('planted_fresh',json.dumps(aggregate)));c.close()
 print(json.dumps(aggregate),flush=True)
if __name__=='__main__':main()
