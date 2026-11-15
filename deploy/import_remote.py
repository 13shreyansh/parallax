"""Load the private export through the container's Unix socket, without public SQL."""
import gzip,json,subprocess,sys,base64,pathlib
TABLES={'theme','topic','topic_theme','article','claim','cited_source','source_chunk','claim_source','claim_group','judgment','flag','revision','evaluation','quality_exclusion','independent_review','claim_rendering','flag_rendering'}
def lit(v):
 if v is None:return 'NULL'
 if isinstance(v,bool):return '1' if v else '0'
 if isinstance(v,(int,float)):return repr(v)
 if isinstance(v,dict):
  if '$bytes' in v:return "FROM_BASE64('"+v['$bytes']+"')"
  if '$datetime' in v:v=v['$datetime'].replace('T',' ')
  else:v=json.dumps(v,ensure_ascii=False)
 return "'"+str(v).replace('\\','\\\\').replace("'","\\'").replace('\0','\\0').replace('\n','\\n').replace('\r','\\r')+"'"
child=subprocess.Popen(['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot --default-character-set=utf8mb4 --max-allowed-packet=128M'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def write(s):child.stdin.write(s.encode('utf-8'))
write("USE parallax; SET time_zone='+00:00'; SET system_versioning_insert_history=1;\n")
counts={}
with gzip.open(sys.argv[1],'rt',encoding='utf-8') as f:
 for line in f:
  entry=json.loads(line);table=entry['table'];row=entry['row']
  if table not in TABLES:raise ValueError('Unexpected table')
  if table=='revision' and row.get('row_end',{}).get('$datetime','')[:4]>='2037':row.pop('row_end')
  cols=','.join('`'+k+'`' for k in row);values=','.join(lit(v) for v in row.values())
  write(('INSERT IGNORE' if table=='revision' else 'REPLACE')+' INTO `'+table+'` ('+cols+') VALUES ('+values+');\n')
  counts[table]=counts.get(table,0)+1
child.stdin.close();out=child.stdout.read();err=child.stderr.read();code=child.wait()
if code:print(err.decode()[-3000:]);raise SystemExit(code)
print(json.dumps({'imported':counts}))
