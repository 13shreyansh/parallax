"""Check extracted quotations against actual MediaWiki-rendered revision text."""
import json,re,html,pathlib,concurrent.futures
from lxml import html as lhtml
from .common import db,wiki,WORK,digest,now

def canonical(text):return re.sub(r'\s+','',html.unescape(text)).replace('\u200b','')
def main():
 c=db();q=c.cursor();q.execute('SELECT qid,lang,page_id,rev_id FROM article WHERE qid IN (SELECT DISTINCT qid FROM claim)');articles=q.fetchall();q.execute('SELECT id,qid,lang,rev_id,text FROM claim');claims=q.fetchall();q.execute('SELECT id,payload FROM published_flag');flags=q.fetchall();c.close();directory=WORK/'rendered-revisions';directory.mkdir(exist_ok=True)
 def fetch(a):
  path=directory/f'{a["lang"]}-{a["rev_id"]}.json'
  if path.exists():return json.loads(path.read_text())
  try:
   result=wiki(a['lang'],{'action':'parse','oldid':a['rev_id'],'prop':'text','disableeditsection':1});soup=lhtml.fromstring(result['parse']['text'])
   for node in soup.xpath('//script|//style|//*[contains(concat(" ",normalize-space(@class)," ")," reference ") or contains(concat(" ",normalize-space(@class)," ")," mw-editsection ") or contains(concat(" ",normalize-space(@class)," ")," noprint ")]'):node.drop_tree()
   text=soup.text_content();out={**a,'text':text,'sha256':digest(text),'fetched_at':now()};path.write_text(json.dumps(out,ensure_ascii=False));return out
  except Exception as e:return {**a,'error_type':type(e).__name__}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:docs=list(pool.map(fetch,articles))
 lookup={(a['qid'],a['lang'],a['rev_id']):a for a in docs if 'text' in a};canon={k:canonical(v['text']) for k,v in lookup.items()};rows=[]
 for cl in claims:
  k=(cl['qid'],cl['lang'],cl['rev_id']);rows.append({'claim_id':cl['id'],'exact_rendered':canonical(cl['text']) in canon[k] if k in canon else None,'rev_id':cl['rev_id'],'rendered_sha256':lookup[k]['sha256'] if k in lookup else None})
 matches={r['claim_id']:r['exact_rendered'] for r in rows};flagrows=[]
 for row in flags:
  f=json.loads(row['payload']);fail=[l for l,v in f['versions'].items() if matches.get(v.get('claim_id',v.get('id'))) is not True];flagrows.append({'flag_id':row['id'],'all_quoted_versions_exact':not fail,'failed_languages':fail})
 out={'checked_at':now(),'articles':len(articles),'rendered':len(lookup),'failed_articles':[{k:v for k,v in a.items() if k!='text'} for a in docs if 'text' not in a],'claims':rows,'flags':flagrows};(WORK/'rendered-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({'articles':len(articles),'rendered':len(lookup),'exact_claims':sum(r['exact_rendered'] is True for r in rows),'nonmatching_claims':sum(r['exact_rendered'] is False for r in rows),'unavailable_claims':sum(r['exact_rendered'] is None for r in rows),'published_flags_with_nonmatching_versions':[r for r in flagrows if not r['all_quoted_versions_exact']]}),flush=True)
if __name__=='__main__':main()
