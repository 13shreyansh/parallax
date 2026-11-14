"""Export only the active theme. Full documents travel privately, never as public assets."""
import gzip,json,base64,datetime
import pymysql
from .common import db,WORK

QUERIES={
 'theme':"SELECT * FROM theme WHERE slug='finland-second-world-war'",
 'topic':"SELECT * FROM topic WHERE qid IN (SELECT qid FROM topic_theme WHERE theme='finland-second-world-war')",
 'topic_theme':"SELECT * FROM topic_theme WHERE theme='finland-second-world-war'",
 'article':"SELECT * FROM article WHERE qid IN (SELECT qid FROM topic_theme WHERE theme='finland-second-world-war')",
 'claim':'SELECT * FROM claim',
 'cited_source':'SELECT * FROM cited_source WHERE id IN (SELECT cs.source_id FROM claim_source cs JOIN claim cl ON cl.id=cs.claim_id)',
 'source_chunk':"SELECT * FROM source_chunk WHERE source_id IN (SELECT cs.source_id FROM claim_source cs JOIN claim cl ON cl.id=cs.claim_id) AND source_id IN (SELECT id FROM cited_source WHERE status='Read')",
 'claim_source':'SELECT cs.* FROM claim_source cs JOIN claim cl ON cl.id=cs.claim_id',
 'claim_group':'SELECT * FROM claim_group',
 'judgment':'SELECT * FROM judgment',
 'flag':'SELECT * FROM flag',
 'revision':'SELECT lang,page_id,qid,rev_id,title,text,comment,row_start,row_end FROM revision FOR SYSTEM_TIME ALL',
 'evaluation':'SELECT * FROM evaluation'}
def encode(o):
 if isinstance(o,(datetime.datetime,datetime.date)):return {'$datetime':o.isoformat()}
 if isinstance(o,bytes):return {'$bytes':base64.b64encode(o).decode()}
 raise TypeError(type(o).__name__)
def main():
 c=db();counts={}
 with gzip.open(WORK/'hosted-data.jsonl.gz','wt',encoding='utf-8',compresslevel=5) as out:
  for table,sql in QUERIES.items():
   count=0
   with c.cursor(pymysql.cursors.SSDictCursor) as cur:
    cur.execute(sql)
    for row in cur:
     out.write(json.dumps({'table':table,'row':row},ensure_ascii=False,default=encode)+'\n');count+=1
   counts[table]=count;print(table,count,flush=True)
 (WORK/'hosted-export-counts.json').write_text(json.dumps(counts,indent=2));c.close()
if __name__=='__main__':main()
