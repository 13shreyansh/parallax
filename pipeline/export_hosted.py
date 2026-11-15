"""Export only the active theme. Full documents travel privately, never as public assets."""
import gzip,json,base64,datetime,argparse
import pymysql
from .common import db,WORK

QUERIES={
 'theme':"SELECT * FROM theme WHERE slug='finland-second-world-war'",
 'topic':"SELECT * FROM topic WHERE qid IN (SELECT qid FROM topic_theme WHERE theme='finland-second-world-war')",
 'topic_theme':"SELECT * FROM topic_theme WHERE theme='finland-second-world-war'",
 'article':"SELECT * FROM article WHERE qid IN (SELECT qid FROM topic_theme WHERE theme='finland-second-world-war')",
 'claim':'SELECT * FROM claim',
 'claim_rendering':'SELECT * FROM claim_rendering',
 'flag_rendering':'SELECT * FROM flag_rendering',
 'cited_source':'SELECT * FROM cited_source WHERE id IN (SELECT cs.source_id FROM claim_source cs JOIN claim cl ON cl.id=cs.claim_id)',
 'source_chunk':"SELECT * FROM source_chunk WHERE source_id IN (SELECT cs.source_id FROM claim_source cs JOIN claim cl ON cl.id=cs.claim_id) AND source_id IN (SELECT id FROM cited_source WHERE status='Read')",
 'claim_source':'SELECT cs.* FROM claim_source cs JOIN claim cl ON cl.id=cs.claim_id',
 'claim_group':'SELECT * FROM claim_group',
 'judgment':'SELECT * FROM judgment',
 'flag':'SELECT * FROM flag',
 'revision':'SELECT lang,page_id,qid,rev_id,title,text,comment,row_start,row_end FROM revision FOR SYSTEM_TIME ALL',
 'evaluation':'SELECT * FROM evaluation',
 'quality_exclusion':'SELECT * FROM quality_exclusion',
 'independent_review':'SELECT * FROM independent_review'}
def encode(o):
 if isinstance(o,(datetime.datetime,datetime.date)):return {'$datetime':o.isoformat()}
 if isinstance(o,bytes):return {'$bytes':base64.b64encode(o).decode()}
 raise TypeError(type(o).__name__)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--tables');parser.add_argument('--output',default=str(WORK/'hosted-data.jsonl.gz'));parser.add_argument('--non-winter-history',action='store_true');parser.add_argument('--publish-ready',action='store_true');args=parser.parse_args()
 selected=args.tables.split(',') if args.tables else list(QUERIES)
 if not set(selected).issubset(QUERIES):raise ValueError('Unknown export table')
 c=db();counts={}
 with gzip.open(args.output,'wt',encoding='utf-8',compresslevel=5) as out:
  for table in selected:
   sql=QUERIES[table]
   if table=='revision' and args.non_winter_history:sql+=" WHERE qid<>'Q134949'"
   count=0
   with c.cursor(pymysql.cursors.SSDictCursor) as cur:
    cur.execute(sql)
    for row in cur:
     if table=='flag' and args.publish_ready and row['shown']:
      payload=json.loads(row['payload']);row['shown']=int(bool(payload.get('note_model') and payload.get('finalized_at')))
     out.write(json.dumps({'table':table,'row':row},ensure_ascii=False,default=encode)+'\n');count+=1
   counts[table]=count;print(table,count,flush=True)
 (WORK/'hosted-export-counts.json').write_text(json.dumps(counts,indent=2));c.close()
if __name__=='__main__':main()
