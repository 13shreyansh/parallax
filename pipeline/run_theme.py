"""One owner, one bounded scheduler for the default theme; no full-corpus pass."""
import concurrent.futures,json,re
from .common import db,WORK,now
from .check import build_groups,process_batch
from .prompts import VERSION

def main():
    c=db();cur=c.cursor();cur.execute("SELECT qid FROM topic_theme WHERE theme='finland-second-world-war' ORDER BY qid<>'Q134949',qid");qids=[r['qid'] for r in cur.fetchall()]
    cur.execute("SELECT DISTINCT cs.claim_id FROM claim_source cs JOIN cited_source s ON s.id=cs.source_id WHERE s.status='Read'");read={r['claim_id'] for r in cur.fetchall()}
    batches=[]
    for qid in qids:
        groups=build_groups(qid);cur.execute("SELECT id,checks FROM claim_group WHERE qid=%s AND JSON_UNQUOTE(JSON_EXTRACT(checks,'$.prompt_version'))=%s",(qid,VERSION));done={r['id']:json.loads(r['checks']) for r in cur.fetchall()}
        priorities={0:[],1:[],2:[]}
        for g in groups:
            # Source recovery changed evidence. Re-evaluate readable anchors once in this run.
            previous=done.get(g['id'])
            if previous and g['anchor_id'] not in read:continue
            anchor=next(r for rs in g['candidates'].values() for r in rs if r['id']==g['anchor_id'])
            p=0 if g['anchor_id'] in read else 1 if re.search(r'\d',anchor['text']) else 2
            priorities[p].append(g)
        for p,gs in priorities.items():
            for i in range(0,len(gs),8):batches.append((p,qid!='Q134949',qid,gs[i:i+8]))
        print('Prepared',qid,len(groups),'groups',flush=True)
    batches.sort(key=lambda b:b[:3]);c.close();print('Batches',len(batches),flush=True)
    def work(batch):
        # Respect the Phase A time box. Already-running requests can finish and be cached.
        from datetime import datetime
        from zoneinfo import ZoneInfo
        t=datetime.now(ZoneInfo('Europe/Helsinki'))
        if t.hour>=2 and (t.hour>2 or t.minute>=30):return
        try:process_batch(batch[3])
        except Exception as e:
            with open(WORK/'theme-errors.jsonl','a') as f:f.write(json.dumps({'qid':batch[2],'at':now(),'error_type':type(e).__name__})+'\n')
            print('Batch requires retry',batch[2],type(e).__name__,flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:list(pool.map(work,batches))
    print('Theme pass finished or reached Phase A time box',flush=True)

if __name__=='__main__':main()
