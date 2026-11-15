"""Complete only already queued active-theme groups; never repeat completed groups."""
import json,concurrent.futures
from .common import db
from .check import ALIGN_SQL,process_batch

def main():
 c=db();cur=c.cursor();cur.execute("SELECT * FROM claim_group WHERE JSON_EXTRACT(checks,'$.first_pass') IS NULL ORDER BY qid,ordinal");pending=cur.fetchall();groups=[]
 for g in pending:
  cur.execute('SELECT * FROM claim WHERE id=%s',(g['anchor_id'],));anchor=cur.fetchone()
  if not anchor:continue
  candidates={anchor['lang']:[anchor]};cur.execute("SELECT lang FROM article WHERE qid=%s AND lang IN ('fi','sv','en')",(g['qid'],));langs=[r['lang'] for r in cur.fetchall()]
  for lang in langs:
   if lang!=anchor['lang']:cur.execute(ALIGN_SQL,(anchor['id'],g['qid'],lang));candidates[lang]=cur.fetchall()
  groups.append({'id':g['id'],'qid':g['qid'],'anchor_id':g['anchor_id'],'ordinal':g['ordinal'],'candidates':candidates})
 c.close();batches=[]
 for qid in dict.fromkeys(g['qid'] for g in groups):
  gs=[g for g in groups if g['qid']==qid]
  for i in range(0,len(gs),1):batches.append(gs[i:i+1])
 print('Finishing previously queued groups',len(groups),'batches',len(batches),flush=True)
 def work(batch):
  try:process_batch(batch)
  except Exception as e:print('Pending batch requires review',batch[0]['qid'],type(e).__name__,flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(work,batches))
 print('Pending completion pass finished',flush=True)
if __name__=='__main__':main()
