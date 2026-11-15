"""Build beside the live release; Traefik switches only after health succeeds."""
import json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path('/opt/parallax/source');sha=sys.argv[1]
assert len(sha)==40 and all(c in '0123456789abcdef' for c in sha)
def command(args,**kw):return subprocess.run(args,check=True,**kw)
def inspected(name):return json.loads(subprocess.check_output(['docker','inspect',name]))[0]
old=inspected('parallax-api');assert old['Config']['Labels']['io.parallax.owner']=='mariadb-junction'
env=dict(v.split('=',1) for v in old['Config']['Env']);env['PARALLAX_COMMIT']=sha
# A new credential arrives on stdin, never in arguments or files; later releases inherit it from the running container.
if '--stdin-env' in sys.argv:env.update({k:v for k,v in json.load(sys.stdin).items() if k in ['GEMINI_API_KEY']})
# Retain hashed assets for tabs opened on the previous release.
assets=ROOT/'deploy/previous-assets';assets.mkdir(exist_ok=True)
names=subprocess.check_output(['docker','ps','--filter','label=io.parallax.owner=mariadb-junction','--filter','label=io.parallax.release','--format','{{.Names}}'],text=True).splitlines()
for previous in ['parallax-api',*names]:
 command(['docker','cp',previous+':/app/frontend/assets/.',str(assets)],stdout=subprocess.DEVNULL)
command(['docker','compose','-p','parallax','-f',str(ROOT/'deploy/compose.yml'),'build','api'],env={**os.environ,'PARALLAX_COMMIT':sha},stdout=subprocess.DEVNULL)
command(['sh',str(ROOT/'deploy/verify-image.sh')],stdout=subprocess.DEVNULL)
def sql(text):
 r=subprocess.run(['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot --default-character-set=utf8mb4'],input=text,capture_output=True,text=True)
 if r.returncode:raise RuntimeError('Parallax schema migration failed')
sql((ROOT/'pipeline/schema.sql').read_text())
sql("GRANT SELECT,INSERT,UPDATE ON parallax.review_write_marker TO 'parallax_writer'@'localhost';")
sql("GRANT SELECT,INSERT ON parallax.ask_answer TO 'parallax_writer'@'localhost';")
name='parallax-release-'+sha[:10];router='parallax'+sha[:10]
args=['docker','run','-d','--name',name,'--network','bridge','--read-only','--tmpfs','/tmp','--cap-drop','ALL','--security-opt','no-new-privileges:true','--restart','unless-stopped','--memory','2g','--cpus','1.5','-v','parallax_socket:/run/mysqld:ro','--health-cmd',"python -c \"import urllib.request;urllib.request.urlopen('http://127.0.0.1:18808/api/parallax?mode=search&q=Winter%20War',timeout=25)\"",'--health-interval','5s','--health-timeout','30s','--health-retries','3']
for k in ['PARALLAX_DB_USER','PARALLAX_DB_PASSWORD','PARALLAX_WRITER_USER','PARALLAX_WRITER_PASSWORD','PARALLAX_BRIDGE_TOKEN','PARALLAX_COMMIT']+[k for k in ['GEMINI_API_KEY'] if env.get(k)]:args+=['-e',k]
labels={'io.parallax.owner':'mariadb-junction','io.parallax.release':sha,'traefik.enable':'true',f'traefik.http.routers.{router}.entrypoints':'websecure',f'traefik.http.routers.{router}.rule':'Host(`parallax.72.61.22.106.sslip.io`)',f'traefik.http.routers.{router}.service':router,f'traefik.http.routers.{router}.priority':str(int(time.time())),f'traefik.http.routers.{router}.tls':'true',f'traefik.http.routers.{router}.tls.certresolver':'letsencrypt',f'traefik.http.services.{router}.loadbalancer.server.port':'18808'}
for k,v in labels.items():args+=['--label',k+'='+v]
args+=['parallax-api:current'];command(args,env={**os.environ,**env},stdout=subprocess.DEVNULL)
for _ in range(30):
 if inspected(name)['State'].get('Health',{}).get('Status')=='healthy':break
 time.sleep(2)
else:raise RuntimeError('New release did not become healthy; previous release remains available')
print(json.dumps({'release':name,'commit':sha,'healthy':True}))
