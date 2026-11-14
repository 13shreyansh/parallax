import os
import pymysql
from pipeline.common import ROOT,RetryingCursor

def writer_db():
    kwargs=dict(user=os.environ.get('PARALLAX_WRITER_USER',os.environ.get('USER','shreyansh')),password=os.environ.get('PARALLAX_WRITER_PASSWORD',''),database='parallax',charset='utf8mb4',autocommit=True,cursorclass=RetryingCursor,init_command="SET time_zone='+00:00'")
    if os.environ.get('PARALLAX_DB_HOST'):kwargs.update(host=os.environ['PARALLAX_DB_HOST'],port=int(os.environ.get('PARALLAX_DB_PORT','3306')),ssl_ca=os.environ['PARALLAX_DB_CA'],ssl_verify_cert=True,ssl_verify_identity=True)
    else:kwargs['unix_socket']=os.environ.get('PARALLAX_DB_SOCKET',str(ROOT/'work/mariadb.sock'))
    return pymysql.connect(**kwargs)
