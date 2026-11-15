"""Runs only on the authorized VPS. Secrets stay in process/container environments."""
import sys,json,os,secrets,subprocess,time,pathlib
ROOT=pathlib.Path('/opt/parallax/source')
cfg=json.load(sys.stdin)
def inspect(name):
    r=subprocess.run(['docker','inspect',name],capture_output=True,text=True)
    return json.loads(r.stdout)[0] if r.returncode==0 else None
old=inspect('parallax-db');api=inspect('parallax-api')
for obj in [old,api]:
    if obj and obj['Config'].get('Labels',{}).get('io.parallax.owner')!='mariadb-junction':raise RuntimeError('Container name belongs to another service')
oldenv=dict(v.split('=',1) for v in old['Config']['Env']) if old else {}
apienv=dict(v.split('=',1) for v in api['Config']['Env']) if api else {}
env={**os.environ,'PARALLAX_ROOT_PASSWORD':oldenv.get('MARIADB_ROOT_PASSWORD') or secrets.token_urlsafe(36),'PARALLAX_READ_PASSWORD':apienv.get('PARALLAX_DB_PASSWORD') or secrets.token_urlsafe(36),'PARALLAX_WRITER_PASSWORD':apienv.get('PARALLAX_WRITER_PASSWORD') or secrets.token_urlsafe(36),'PARALLAX_BRIDGE_TOKEN':cfg['bridge_token'],'PARALLAX_COMMIT':cfg['commit']}
def safe(s):
    for k,v in env.items():
        if k.startswith('PARALLAX_') and ('PASSWORD' in k or 'TOKEN' in k):s=s.replace(v,'[redacted]')
    return s
r=subprocess.run(['docker','compose','-p','parallax','-f',str(ROOT/'deploy/compose.yml'),'up','-d','--build'],env=env,capture_output=True,text=True)
if r.returncode:
    print(safe((r.stdout+r.stderr)[-6000:]));raise SystemExit(r.returncode)
subprocess.run(['sh',str(ROOT/'deploy/verify-image.sh')],check=True)
def sql(text):
    r=subprocess.run(['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot --default-character-set=utf8mb4'],input=text,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(safe(r.stderr[-1500:]))
    return r.stdout
for _ in range(120):
    try:sql('SELECT 1;');break
    except RuntimeError:time.sleep(1)
else:raise RuntimeError('Parallax database did not start')
sql((ROOT/'pipeline/schema.sql').read_text())
sql("CREATE USER IF NOT EXISTS 'parallax_read'@'localhost' IDENTIFIED BY '"+env['PARALLAX_READ_PASSWORD']+"'; ALTER USER 'parallax_read'@'localhost' IDENTIFIED BY '"+env['PARALLAX_READ_PASSWORD']+"'; GRANT SELECT ON parallax.* TO 'parallax_read'@'localhost'; CREATE USER IF NOT EXISTS 'parallax_writer'@'localhost' IDENTIFIED BY '"+env['PARALLAX_WRITER_PASSWORD']+"'; ALTER USER 'parallax_writer'@'localhost' IDENTIFIED BY '"+env['PARALLAX_WRITER_PASSWORD']+"'; GRANT SELECT ON parallax.flag TO 'parallax_writer'@'localhost'; GRANT SELECT,INSERT,UPDATE ON parallax.editor_reviews TO 'parallax_writer'@'localhost'; GRANT SELECT,INSERT,UPDATE ON parallax.note_copies TO 'parallax_writer'@'localhost'; GRANT SELECT,INSERT,UPDATE ON parallax.review_write_marker TO 'parallax_writer'@'localhost';")
print(json.dumps({'ok':True,'database':'parallax-db','api':'parallax-api','origin':'https://parallax.72.61.22.106.sslip.io','sql_public':False}))
