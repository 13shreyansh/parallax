import os, pathlib, pymysql

ROOT = pathlib.Path(__file__).resolve().parents[1]


def connect(database="npov"):
    kwargs = (
        {
            "host": os.environ["DB_HOST"],
            "port": int(os.environ.get("DB_PORT", "3306")),
            "password": os.environ.get("DB_PASSWORD", ""),
        }
        if os.environ.get("DB_HOST")
        else {
            "unix_socket": os.environ.get("DB_SOCKET", str(ROOT / "work/mariadb.sock"))
        }
    )
    return pymysql.connect(
        **kwargs,
        user=os.environ.get("DB_USER", os.environ.get("USER", "shreyansh")),
        database=database,
        charset="utf8mb4",
        init_command="SET time_zone='+00:00'",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


ALIGN_SQL = """SELECT id, text, section, rev_id, page_id, lang,
 VEC_DISTANCE_COSINE(embedding,VEC_FromText(%s)) AS distance
 FROM passage WHERE qid=%s AND lang=%s
 ORDER BY distance LIMIT 3"""
HISTORY_SQL = """SELECT lang,page_id,rev_id,title,row_start AS revised_at,
 CHAR_LENGTH(text) AS characters FROM revision FOR SYSTEM_TIME ALL
 WHERE lang=%s AND page_id=%s ORDER BY row_start DESC LIMIT 40"""
ASOF_SQL = """SELECT lang,page_id,rev_id,title,text,row_start AS revised_at
 FROM revision FOR SYSTEM_TIME AS OF TIMESTAMP %s
 WHERE lang=%s AND page_id=%s"""
