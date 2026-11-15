"""Mean native cosine distance across actual prose claims in fi/sv/en only."""
import concurrent.futures,json
from .common import db,init_db,WORK,now
SQL='SELECT VEC_DISTANCE_COSINE(peer.embedding,VEC_FromText(%s)) distance FROM readable_claim peer WHERE peer.qid=%s AND peer.lang=%s ORDER BY distance LIMIT 1'
def topic(qid):
 c=db();q=c.cursor();q.execute("SELECT id,lang,VEC_ToText(embedding) vector_text FROM readable_claim WHERE qid=%s AND lang IN ('fi','sv','en')",(qid,));rows=q.fetchall();distances=[]
 for r in rows:
  for lang in ['fi','sv','en']:
   if lang==r['lang']:continue
   q.execute(SQL,(r['vector_text'],qid,lang));v=q.fetchone()
   if v:distances.append(min(1,max(0,float(v['distance']))))
 value=100*sum(distances)/len(distances) if distances else None;q.execute('UPDATE topic SET distance=%s WHERE qid=%s',(value,qid));c.close();print(qid,value,flush=True);return {'qid':qid,'distance':value,'prose_claims':len(rows),'pair_count':len(distances)}
def main():
 init_db();c=db();q=c.cursor();q.execute("SELECT qid FROM topic_theme WHERE theme='finland-second-world-war'");ids=[r['qid'] for r in q.fetchall()];c.close()
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as p:rows=list(p.map(topic,ids))
 (WORK/'distance-prose.json').write_text(json.dumps({'measured_at':now(),'query':SQL,'topics':rows},indent=2))
if __name__=='__main__':main()
