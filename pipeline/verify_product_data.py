"""Read-only checks against the deployed response and corresponding stored evidence."""
import json,random,requests,pathlib
from .common import db,ROOT
from .text import normalize
from service.app import temporal_query
BASE='https://parallax-gamma-red.vercel.app'
def main():
 c=db();cur=c.cursor();article=requests.get(BASE+'/api/parallax',params={'mode':'article','qid':'Q134949'},timeout=60).json();method=requests.get(BASE+'/api/parallax',params={'mode':'method'},timeout=60).json();flags=article['flags'];random.Random(2026111514).shuffle(flags);checks=[]
 for f in flags[:10]:
  cur.execute('SELECT wikitext FROM article WHERE qid=%s AND lang=%s',(f['qid'],f['language']));text=cur.fetchone()['wikitext'];claim=f['versions'][f['language']]['text'];exact=normalize(claim) in normalize(text)
  source=None
  if f.get('source'):
   cur.execute('SELECT text,status FROM cited_source WHERE id=%s',(f['source']['id'],));s=cur.fetchone();source=s['status']=='Read' and f['source']['passage'] in s['text']
  checks.append({'id':f['id'],'exact_claim_in_stored_revision':exact,'exact_read_source_passage':source});assert exact and source is not False
 dates=['2010-01-01','2012-11-27','2012-11-28','2020-01-01','2025-01-01'];history=[]
 for day in dates:
  result=requests.get(BASE+'/api/parallax',params={'mode':'article','qid':'Q134949','flag':'65c3491c5d1f63e938fe4b3e32617dc9','asof':day},timeout=60).json();traces=result['queries'];query=next(t for t in traces if t['name'].startswith('As of '));assert 'FOR SYSTEM_TIME AS OF' in query['sql']
  cur.execute(*temporal_query(result['versions'],day+' 23:59:59'));stored={r['lang']:r for r in cur.fetchall()}
  for group in result['groups']:
   for lang,v in group['versions'].items():
    if v.get('asof_text'):
     revision=stored.get(lang);assert revision and revision['rev_id']==v['asof_revision'] and normalize(v['asof_text']) in normalize(revision['text'])
  history.append({'date':day,'database_ms':query['ms'],'revision_ids':result['asof_revisions'],'returned_text_matches':True})
 cur.execute('SELECT COUNT(*) claims FROM claim');claims=cur.fetchone()['claims'];cur.execute('SELECT COUNT(*) flags FROM published_flag');count=cur.fetchone()['flags'];assert method['counts']['claims']==claims and method['counts']['flags']==count
 out={'public_origin':BASE,'health':requests.get(BASE+'/api/parallax?mode=health').json(),'quotes':checks,'historical_dates':history,'counts_match_sql':True,'counts':method['counts']};(ROOT/'artifacts/verification/data.json').write_text(json.dumps(out,default=str,indent=2));print(json.dumps({'quotes':len(checks),'dates':history,'counts':method['counts']},default=str));c.close()
if __name__=='__main__':main()
