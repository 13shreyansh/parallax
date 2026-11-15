"""Nightly real-search validation. Failed examples are hidden, never substituted answers."""
import datetime,json,subprocess,urllib.request,urllib.parse,sys
origin=sys.argv[1] if len(sys.argv)>1 else 'https://parallax.72.61.22.106.sslip.io'
questions=[('en','How many Soviet soldiers died in the Winter War?'),('fi','Kuinka monta ruotsalaista vapaaehtoista taisteli talvisodassa?'),('sv','När slutade vinterkriget?'),('fi','Milloin talvisota päättyi?'),('en','When did the Winter War begin?')]
def literal(s):return "'"+s.replace('\\','\\\\').replace("'","\\'")+"'"
sql=['USE parallax; UPDATE ask_example SET passed=0;'];passed=[]
for i,(lang,q) in enumerate(questions):
 try:
  with urllib.request.urlopen(origin+'/api/parallax?'+urllib.parse.urlencode({'mode':'search','q':q}),timeout=90) as r:data=json.load(r)
  count=len((data.get('group') or {}).get('versions',{}));ok=count>=2
 except Exception:count=0;ok=False
 sql.append('REPLACE INTO ask_example VALUES ('+','.join([literal('example-'+str(i)),literal(lang),literal(q),str(i),str(int(ok)),str(count),'UTC_TIMESTAMP()'])+');')
 if ok:passed.append({'lang':lang,'versions':count})
r=subprocess.run(['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot --default-character-set=utf8mb4'],input='\n'.join(sql),text=True,capture_output=True)
if r.returncode:raise RuntimeError('Example validation could not be stored')
print(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':passed}))
