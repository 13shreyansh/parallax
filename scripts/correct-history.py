"""Reimport with an explicit archive cutoff. Never fill an unobserved revision gap."""
import sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pyarrow.parquet as pq
from server.db import connect
articles=json.load(open(ROOT/'work/current-articles.json'));wanted=[a['page_id'] for a in articles if a['lang']=='fi'];history={}
for p in sorted((ROOT/'work/official/m').glob('*.parquet')):
 for r in pq.read_table(p,filters=[('page_id','in',wanted)],columns=['page_id','title','rev_id','timestamp','text']).to_pylist():history.setdefault(('fi',r['page_id']),{})[r['rev_id']]={**r,'archive':True}
for a in articles:
 h=history.setdefault((a['lang'],a['page_id']),{})
 for r in a['revisions']:h[r['revid']]={'rev_id':r['revid'],'title':a['title'],'timestamp':r['timestamp'],'text':r['slots']['main']['*']}
con=connect();c=con.cursor();c.execute('RENAME TABLE revision TO revision_initial_import')
for stmt in (ROOT/'schema.sql').read_text().split(';'):
 if stmt.strip():c.execute(stmt)
c.execute("SET time_zone='+00:00'");c.execute('SET system_versioning_insert_history=1')
coverage={}
for (lang,pid),vs in history.items():
 rows=sorted(vs.values(),key=lambda r:str(r['timestamp']));live=[r['timestamp'] for r in rows if not r.get('archive')]
 coverage[f'{lang}-{pid}']={'archive_through':'2026-10-01T00:00:00Z' if lang=='fi' else None,'recent_from':min(live) if live else None}
 for i,r in enumerate(rows):
  ts=str(r['timestamp']).replace('T',' ').replace('Z','').replace('+00:00','');end=str(rows[i+1]['timestamp']).replace('T',' ').replace('Z','').replace('+00:00','') if i+1<len(rows) else None
  if r.get('archive') and (not end or end>'2026-10-01 00:00:00'):end='2026-10-01 00:00:00'
  if end and end<=ts:continue
  vals=(lang,pid,r['rev_id'],r['title'],r['text'],ts)
  if end:c.execute('INSERT INTO revision(lang,page_id,rev_id,title,text,row_start,row_end) VALUES (%s,%s,%s,%s,%s,%s,%s)',vals+(end,))
  else:c.execute('INSERT INTO revision(lang,page_id,rev_id,title,text,row_start) VALUES (%s,%s,%s,%s,%s,%s)',vals)
json.dump(coverage,open(ROOT/'data/history-coverage.json','w'),indent=2)
c.execute('SELECT COUNT(*) AS n FROM revision FOR SYSTEM_TIME ALL');print('Corrected history intervals:',c.fetchone()['n'])
