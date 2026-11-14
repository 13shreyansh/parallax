"""New article families, reserved before labels or detector output."""
import json,re,random,concurrent.futures
from .common import WORK,ROOT,digest,now
from .extract import split_claims
from .sources import fetch_source,book_preview

def main():
 old=json.loads((ROOT/'eval/parallax/FROZEN.json').read_text());excluded={x['article']['qid'] for x in old['case_metadata']}
 manifest=json.loads((WORK/'manifest.json').read_text());eligible=[r for r in manifest if 'finland-second-world-war' not in r['themes'] and r['qid'] not in excluded];random.Random(2026111506).shuffle(eligible)
 candidates=[];seen=set()
 for topic in eligible:
  a=topic['versions']['en'];path=WORK/'articles'/f'en-{a["page_id"]}.json'
  if not path.exists():continue
  article=json.loads(path.read_text())
  for cl in split_claims(article):
   urls=[u for ref in cl['citations'] for u in ref['urls'] if not book_preview(u) and 'wikipedia.org' not in u and 'web.archive.org' not in u]
   if not urls or not 70<=len(cl['text'])<=450 or not re.search(r'\b\d{2,4}\b',cl['text']):continue
   url=urls[0]
   if url in seen:continue
   seen.add(url);candidates.append({'id':digest(['fresh-heldout',cl['id']])[:32],'article':{k:article[k] for k in ['qid','title','lang','rev_id','page_id']},'claim':cl,'url':url})
   if len(candidates)>=300:break
  if len(candidates)>=300:break
 directory=WORK/'eval-fresh';directory.mkdir(exist_ok=True)
 reservation={'created_at':now(),'seed':2026111506,'excluded_previous_article_families':sorted(excluded),'heldout_qids':sorted({x['article']['qid'] for x in candidates}),'detector_output_seen':False}
 (directory/'reservation.json').write_text(json.dumps(reservation,indent=2));queue=[]
 def work(case):
  path=directory/f'{case["id"]}.json'
  if path.exists():return json.loads(path.read_text())
  case['source']=fetch_source(case['url']);path.write_text(json.dumps(case,ensure_ascii=False,indent=2));return case
 with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
  for c in pool.map(work,candidates):
   if c['source']['status']=='Read':queue.append({'id':c['id'],'path':str(directory/f'{c["id"]}.json'),'article':c['article']['title'],'claim':c['claim']['text'],'source':c['source']['title']})
   (directory/'label-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2));print('Fresh source',c['id'],c['source']['status'],'readable',len(queue),flush=True)
 print('Fresh queue ready',len(queue),flush=True)
if __name__=='__main__':main()
