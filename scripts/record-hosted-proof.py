"""Read-only deployed API / direct private SQL / container isolation receipt."""
import ast,inspect,json,subprocess,datetime,pathlib,requests
from service.app import counts
query=ast.literal_eval(ast.parse(inspect.getsource(counts)).body[0].body[0].value)
remote='''import json,subprocess,sys
cfg=json.load(sys.stdin)
def sql(s):
 r=subprocess.run(['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot --batch --raw parallax'],input=s,text=True,capture_output=True)
 if r.returncode:raise RuntimeError('Private SQL receipt failed')
 lines=r.stdout.splitlines();return [dict(zip(lines[0].split('\\t'),row.split('\\t'))) for row in lines[1:]]
db=json.loads(subprocess.check_output(['docker','inspect','parallax-db']))[0]
print(json.dumps({'counts':sql(cfg['query'])[0],'schema_privileges':sql("SELECT GRANTEE,PRIVILEGE_TYPE,TABLE_SCHEMA FROM information_schema.SCHEMA_PRIVILEGES WHERE GRANTEE LIKE '%parallax_%'"),'table_privileges':sql("SELECT GRANTEE,PRIVILEGE_TYPE,TABLE_SCHEMA,TABLE_NAME FROM information_schema.TABLE_PRIVILEGES WHERE GRANTEE LIKE '%parallax_%'"),'database_network':db['HostConfig']['NetworkMode'],'database_ports':db['NetworkSettings']['Ports'],'database_arguments':db['Args'],'groups':sql("SELECT COUNT(*) total,SUM(JSON_EXTRACT(checks,'$.first_pass') IS NOT NULL) checked FROM claim_group")[0],'judgments':sql('SELECT COUNT(*) total FROM judgment')[0],'raw_claims':sql('SELECT COUNT(*) total FROM claim')[0]}))
'''
# SSH transports a public query only; database credentials never leave the container.
import shlex
result=json.loads(subprocess.check_output(['ssh','-o','BatchMode=yes','root@72.61.22.106','python3 -c '+shlex.quote(remote)],input=json.dumps({'query':query}).encode()))
base='https://parallax-gamma-red.vercel.app';api=requests.get(base+'/api/parallax?mode=method',timeout=60).json();health=requests.get(base+'/api/parallax?mode=health',timeout=30).json()
for k in ['articles','themes','versions','claims','sources','sources_read','revisions','flags','dismissed','copied']:assert int(result['counts'][k])==int(api['counts'][k]),k
assert result['database_network']=='none' and '--skip-networking' in result['database_arguments'];assert not any(result['database_ports'].values())
out={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'health':health,'sql':query,'sql_result':result,'api_counts':api['counts'],'counts_match':True,'local_api_stopped':True};pathlib.Path('artifacts/verification/hosted.json').write_text(json.dumps(out,indent=2));print(json.dumps({'counts_match':True,'counts':api['counts'],'private_sql':True,'commit':health['commit']}))
