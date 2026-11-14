import pathlib,sys,json,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from server.db import connect,HISTORY_SQL
j=json.load(open(ROOT/'public/snapshot.json'));c=connect().cursor();out={}
for a in j['articles']:
 v=next(v for v in a['versions'] if v['lang']=='fi');c.execute(HISTORY_SQL,('fi',v['page_id']));rows=c.fetchall()
 for r in rows:r['revised_at']=r['revised_at'].isoformat(sep=' ')
 c.execute('SELECT COUNT(*) AS n FROM revision FOR SYSTEM_TIME ALL WHERE lang=%s AND page_id=%s',('fi',v['page_id']))
 out[a['qid']]={'rows':rows,'total':c.fetchone()['n'],'sql':HISTORY_SQL,'saved':True}
json.dump(out,open(ROOT/'public/history-snapshot.json','w'))
