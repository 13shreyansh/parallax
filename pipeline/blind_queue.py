"""Freeze a reproducible random sample without detector judgments or explanations."""
import json,random,pathlib,hashlib,argparse,gzip
from .common import db,WORK,now

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--hosted');parser.add_argument('--directory',default='blind-real');args=parser.parse_args()
 c=db();cur=c.cursor()
 if args.hosted:rows=json.loads(gzip.open(args.hosted,'rt').read())
 else:cur.execute('SELECT * FROM published_flag ORDER BY id');rows=cur.fetchall()
 seen=set();population=[]
 for r in rows:
  key=(r['claim_id'],r['check_type'],r['verdict'])
  if key in seen:continue
  seen.add(key);population.append(r)
 if len(population)<60:raise RuntimeError('Fewer than 60 unique shown flags')
 seed='parallax-final-blind-2026-11-15-02-20' if args.hosted else 'parallax-blind-2026-11-15-01-16';sample=random.Random(seed).sample(population,60);out=WORK/args.directory;out.mkdir(exist_ok=True)
 manifest={'seed':seed,'sampled_at':now(),'population':len(population),'sample_size':60,'mapping':{},'article_files':{},'source_files':{}}
 for i,r in enumerate(sample,1):
  f=json.loads(r['payload']);case={'case':i,'check_type':f['check'],'language':f['language'],'claim':f['versions'][f['language']]['text'],'versions':{l:{'text':v['text'],'rev_id':v['rev_id']} for l,v in f['versions'].items()},'cited_sources':[]}
  if f.get('missing_language'):case['language_to_check_for_coverage']=f['missing_language']
  cur.execute('SELECT * FROM article WHERE qid=%s AND lang IN (\'fi\',\'sv\',\'en\')',(f['qid'],))
  for a in cur.fetchall():
   key=f'{a["qid"]}-{a["lang"]}';p=out/(key+'.txt');p.write_text(a['wikitext']);manifest['article_files'][key]=str(p);case.setdefault('full_article_files',{})[a['lang']]=str(p)
  cur.execute('SELECT s.id,s.title,s.url,s.status,s.text FROM cited_source s JOIN claim_source cs ON s.id=cs.source_id WHERE cs.claim_id=%s',(f['claim_id'],))
  for s in cur.fetchall():
   p=out/(s['id']+'.txt');p.write_text(s.pop('text') or '');manifest['source_files'][s['id']]=str(p);s['text_file']=str(p);case['cited_sources'].append(s)
  (out/f'case-{i:02}.json').write_text(json.dumps(case,ensure_ascii=False,indent=2));manifest['mapping'][str(i)]=f['id']
 (out/'manifest-private.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps({k:manifest[k] for k in ['seed','population','sample_size','sampled_at']}))
if __name__=='__main__':main()
