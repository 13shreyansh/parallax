"""Prepare independent held-out labels before any held-out detector request."""
import json,random,re,concurrent.futures
from .common import WORK,ROOT,digest,now
from .extract import split_claims
from .sources import fetch_source,chunks,book_preview

def main():
    directory=WORK/'eval';directory.mkdir(exist_ok=True)
    manifest=json.loads((WORK/'manifest.json').read_text());rng=random.Random(2026111502)
    eligible=[r for r in manifest if 'finland-second-world-war' not in r['themes']];rng.shuffle(eligible)
    candidates=[];seen=set()
    for topic in eligible:
        a=topic['versions']['en'];path=WORK/'articles'/f'en-{a["page_id"]}.json'
        if not path.exists():continue
        article=json.loads(path.read_text())
        for cl in split_claims(article):
            urls=[u for ref in cl['citations'] for u in ref['urls'] if not book_preview(u) and 'wikipedia.org' not in u and 'web.archive.org' not in u]
            if not urls or not 70<=len(cl['text'])<=400 or not re.search(r'\b\d{2,4}\b',cl['text']):continue
            url=urls[0]
            if url in seen:continue
            seen.add(url);candidates.append({'id':digest(['heldout',cl['id']])[:32],'article':{k:article[k] for k in ['qid','title','lang','rev_id','page_id']},'claim':cl,'url':url})
            if len(candidates)>=180:break
        if len(candidates)>=180:break
    # Reserve entire article families before fetching or labeling, not just individual sentences.
    reserve={'seed':2026111502,'created_at':now(),'heldout_qids':sorted({r['article']['qid'] for r in candidates}),'development_excluded':['Q134949'],'detector_output_seen':False}
    (directory/'reservation.json').write_text(json.dumps(reserve,indent=2));(ROOT/'eval/parallax').mkdir(exist_ok=True)
    (ROOT/'eval/parallax/reservation.json').write_text(json.dumps(reserve,indent=2))
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        for case,source in zip(candidates,pool.map(fetch_source,[c['url'] for c in candidates])):
            case['source']=source
            print('held-out source',case['id'],source['status'],flush=True)
    readable=[c for c in candidates if c['source']['status']=='Read']
    for case in readable:
        (directory/f'{case["id"]}.json').write_text(json.dumps(case,ensure_ascii=False,indent=2))
    # This is a label queue, not evaluated results. Controls are not assumed clean.
    queue=[{'id':c['id'],'path':str(directory/f'{c["id"]}.json'),'article':c['article']['title'],'claim':c['claim']['text'],'source':c['source']['title']} for c in readable]
    (directory/'label-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2))
    print('Independent label queue',len(queue),'readable claim-source pairs',flush=True)

if __name__=='__main__':main()
