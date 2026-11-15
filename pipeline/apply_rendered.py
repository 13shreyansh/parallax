"""Store literal-rendering proof before enabling the editor-facing views."""
import json,datetime
from .common import db,WORK,init_db
CLAIM_DDL='CREATE TABLE IF NOT EXISTS claim_rendering (claim_id CHAR(32) PRIMARY KEY,rev_id BIGINT NOT NULL,exact_rendered BOOLEAN NOT NULL,rendered_sha256 CHAR(64),checked_at DATETIME NOT NULL)'
FLAG_DDL='CREATE TABLE IF NOT EXISTS flag_rendering (flag_id CHAR(32) PRIMARY KEY,flag_checked_at DATETIME NOT NULL,all_quotes_exact BOOLEAN NOT NULL,checked_at DATETIME NOT NULL)'
def main():
 audit=json.loads((WORK/'rendered-audit.json').read_text());assert audit['rendered']==audit['articles']==68 and not audit['failed_articles'];c=db();q=c.cursor();q.execute(CLAIM_DDL);q.execute(FLAG_DDL)
 for row in audit['claims']:
  assert row['exact_rendered'] is not None
  q.execute('REPLACE INTO claim_rendering VALUES (%s,%s,%s,%s,UTC_TIMESTAMP())',(row['claim_id'],row['rev_id'],row['exact_rendered'],row['rendered_sha256']))
 for row in audit['flags']:
  q.execute('SELECT checked_at FROM flag WHERE id=%s',(row['flag_id'],));time=q.fetchone()['checked_at'];q.execute('REPLACE INTO flag_rendering VALUES (%s,%s,%s,UTC_TIMESTAMP())',(row['flag_id'],time,row['all_quoted_versions_exact']))
 c.close();init_db();c=db();q=c.cursor();q.execute('SELECT COUNT(*) n FROM readable_claim');count=q.fetchone()['n'];q.execute('SELECT COUNT(*) n FROM published_flag');flags=q.fetchone()['n'];c.close()
 result={'checked_at':audit['checked_at'],'articles_rendered':68,'raw_claims':len(audit['claims']),'rendered_matches':sum(r['exact_rendered'] for r in audit['claims']),'editor_claims':count,'nonmatching_records_retained':sum(not r['exact_rendered'] for r in audit['claims']),'shown_flags':flags,'all_shown_quoted_versions_match_rendered_revision':all(r['all_quoted_versions_exact'] for r in audit['flags'])}
 from .common import ROOT
 (ROOT/'artifacts/verification/rendered.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
