"""Restore only writes bearing this test run, preserving concurrent editor changes."""
import json,re,subprocess,sys
cfg=json.load(sys.stdin);run=cfg['run'];assert re.fullmatch('[0-9a-f-]{36}',run)
ids=cfg.get('ids',[]);assert all(re.fullmatch('[0-9a-f]{32}',i) for i in ids)
def literal(s):return 'NULL' if s is None else "'"+str(s).replace('\\','\\\\').replace("'","\\'")+"'"
def sql(s):
 r=subprocess.run(['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot -N --batch --raw parallax'],input=s,text=True,capture_output=True)
 if r.returncode:raise RuntimeError('Scoped test-state operation failed')
 return [json.loads(x) for x in r.stdout.splitlines() if x.startswith('{')]
if cfg['action']=='snapshot':
 rows=sql("SELECT JSON_OBJECT('flag_id',flag_id,'reason',reason,'dismissed',dismissed,'reviewed_at',reviewed_at) FROM editor_reviews WHERE flag_id IN ("+','.join(literal(x) for x in ids)+");")
 print(json.dumps({'reviews':rows}))
else:
 commands=['START TRANSACTION;'];baseline={r['flag_id']:r for r in cfg['baseline']['reviews']}
 for fid in ids:
  # Lock order matches API review's transaction: review first, marker second.
  commands+=['SELECT flag_id FROM editor_reviews WHERE flag_id='+literal(fid)+' FOR UPDATE;','SELECT flag_id FROM review_write_marker WHERE flag_id='+literal(fid)+' FOR UPDATE;']
  own="EXISTS (SELECT 1 FROM review_write_marker m WHERE m.flag_id="+literal(fid)+" AND m.run_id="+literal(run)+")"
  if fid in baseline:
   b=baseline[fid];commands+=['UPDATE editor_reviews SET reason='+literal(b['reason'])+',dismissed='+str(int(b['dismissed']))+',reviewed_at='+literal(b['reviewed_at'])+' WHERE flag_id='+literal(fid)+' AND '+own+';']
  else:commands+=['DELETE FROM editor_reviews WHERE flag_id='+literal(fid)+' AND '+own+';']
  commands+=['DELETE FROM review_write_marker WHERE flag_id='+literal(fid)+' AND run_id='+literal(run)+';']
 for fid,n in cfg.get('copies',{}).items():
  assert re.fullmatch('[0-9a-f]{32}',fid) and isinstance(n,int) and 0<=n<=10
  commands+=['UPDATE note_copies SET copies=GREATEST(0,copies-'+str(n)+') WHERE flag_id='+literal(fid)+';','DELETE FROM note_copies WHERE flag_id='+literal(fid)+' AND copies=0;']
 commands+=['COMMIT;'];sql('\n'.join(commands));print(json.dumps({'restored':True,'run':run}))
