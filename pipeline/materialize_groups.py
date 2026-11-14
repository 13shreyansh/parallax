"""Make every stored article claim readable without pretending it was checked."""
import json
from .common import db
from .check import build_groups

def versions_for(group):
 versions={}
 for lang,rows in group['candidates'].items():
  if rows and (rows[0]['id']==group['anchor_id'] or float(rows[0].get('distance',1))<=.32):
   r=rows[0];versions[lang]={k:r.get(k) for k in ['id','lang','section','text','rev_id','gloss']};versions[lang]['claim_id']=r['id']
 return versions

def main():
 c=db();cur=c.cursor();cur.execute("SELECT qid FROM topic_theme WHERE theme='finland-second-world-war'");qids=[r['qid'] for r in cur.fetchall()]
 for qid in qids:
  groups=build_groups(qid)
  for g in groups:
   versions=versions_for(g)
   cur.execute('INSERT IGNORE INTO claim_group VALUES (%s,%s,%s,%s,%s,%s)',(g['id'],qid,g['anchor_id'],g['ordinal'],json.dumps(versions,ensure_ascii=False),json.dumps({'state':'pending'})))
  print('Materialized all claim rows',qid,len(groups),flush=True)
 c.close()
if __name__=='__main__':main()
