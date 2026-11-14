import subprocess,time,json
BASE=['docker','exec','-i','parallax-db','sh','-c','MYSQL_PWD="$MARIADB_ROOT_PASSWORD" exec mariadb -uroot parallax --batch --raw']
queries=["EXPLAIN SELECT lang,page_id,rev_id,title,text,row_start FROM revision FOR SYSTEM_TIME AS OF TIMESTAMP '2012-11-27 23:59:59' WHERE qid='Q134949'", "EXPLAIN SELECT lang,page_id,rev_id,title,text,row_start FROM revision FOR SYSTEM_TIME AS OF TIMESTAMP '2012-11-27 23:59:59' WHERE lang='fi' AND page_id=2195"]
for q in queries:
 p=subprocess.run(BASE,input=q,text=True,capture_output=True);print(p.stdout or p.stderr)
