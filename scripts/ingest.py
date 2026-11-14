"""Import genuine Wikipedia snapshots, live counterparts, and revision history."""
import sys,pathlib,json,re,time,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import requests,numpy as np,pyarrow.parquet as pq
from sentence_transformers import SentenceTransformer
from server.db import connect,ALIGN_SQL
from server.checks import check,tone,source_state
QIDS=['Q134949','Q122100','Q211855','Q185489','Q152306','Q736268','Q695285','Q154940','Q823175']
def chunks(text):
 section='Introduction';out=[]
 for line in text.splitlines():
  line=line.strip()
  if not line:continue
  if line.startswith('#') or re.match(r'^==',line):
   section=line.strip('#= ');continue
  if line.startswith(('|','- ','* ')) or len(line)<45:continue
  if section.lower() in ['references','sources','external links','see also','lähteet','källor','viitteet','externa länkar']:continue
  for sent in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÅÉ0-9])',line):
   if 55<=len(sent)<=650:out.append((section,sent))
 return out[:100]
def live(r):
 p=ROOT/'work/live'/f"{r['lang']}-{r['page_id']}.json";p.parent.mkdir(exist_ok=True)
 if p.exists():return json.load(open(p))
 try:
  params={'action':'query','format':'json','pageids':r['page_id'],'prop':'extracts|revisions|langlinks','explaintext':1,'rvprop':'ids|timestamp|content','rvslots':'main','rvlimit':3,'lllimit':500}
  resp=requests.get(f"https://{r['lang']}.wikipedia.org/w/api.php",params=params,headers={'User-Agent':'NPOVRadar/0.1 (Junction 2026; https://github.com/13shreyansh/npov-radar)'},timeout=45);resp.raise_for_status()
  page=next(iter(resp.json()['query']['pages'].values()));revs=page['revisions']
  rr={**r,'text':page.get('extract',r['text']),'title':page['title'],'rev_id':revs[0]['revid'],'date_modified':revs[0]['timestamp'],'origin':'Wikipedia API live fetch','revisions':revs,'langlinks':page.get('langlinks',[])}
  if not rr['text']:raise ValueError('Empty extract')
  json.dump(rr,open(p,'w'),ensure_ascii=False);return rr
 except Exception as e:
  print('Live fetch fallback',r['lang'],r['title'],type(e).__name__,flush=True)
  return {**r,'origin':'S dataset, August 2025 snapshot','revisions':[]}
def main():
 con=connect(None);cur=con.cursor()
 for stmt in (ROOT/'schema.sql').read_text().split(';'):
  if stmt.strip():cur.execute(stmt)
 con.close();con=connect();cur=con.cursor()
 rows=[]
 for lang in ['fi','en','sv']:
  rows.extend([r for r in pq.read_table(ROOT/f'work/vector-starter/data/articles-{lang}.parquet').to_pylist() if r['wikidata_id'] in QIDS])
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:articles=list(ex.map(live,rows))
 json.dump(articles,open(ROOT/'work/current-articles.json','w'),ensure_ascii=False)
 print('Fetched',len(articles),'articles',flush=True)
 model=SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',cache_folder=str(ROOT/'work/models'),device='mps')
 passages=[]
 for a in articles:
  cur.execute('REPLACE INTO article VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(a['lang'],a['page_id'],a['wikidata_id'],a['rev_id'],a['title'],a['date_modified'].replace('T',' ').replace('Z',''),a['text'],a['origin']))
  for i,(sec,text) in enumerate(chunks(a['text'])):passages.append({'id':f"{a['lang']}-{a['page_id']}-{i}",'qid':a['wikidata_id'],'lang':a['lang'],'page_id':a['page_id'],'rev_id':a['rev_id'],'ordinal':i,'section':sec,'text':text})
 print('Embedding',len(passages),'passages',flush=True)
 emb=model.encode([p['text'] for p in passages],batch_size=64,normalize_embeddings=True,show_progress_bar=False)
 for p,v in zip(passages,emb):
  cur.execute('REPLACE INTO passage VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(*p.values(),np.asarray(v,dtype='<f4').tobytes()))
 json.dump(passages,open(ROOT/'data/passages.json','w'),ensure_ascii=False)
 np.save(ROOT/'work/embeddings.npy',emb)
 print('Native MariaDB vector rows loaded',flush=True)
 # M is Finnish only; read selected articles with row-group filtering, not all text.
 history={}
 wanted={r['page_id'] for r in rows if r['lang']=='fi'}
 for path in sorted((ROOT/'work/official/m').glob('versions-*.parquet')):
  table=pq.read_table(path,filters=[('page_id','in',list(wanted))],columns=['page_id','title','rev_id','timestamp','text'])
  for r in table.to_pylist():history.setdefault(('fi',r['page_id']),{})[r['rev_id']]={**r,'archive':True}
 for a in articles:
  key=(a['lang'],a['page_id']);h=history.setdefault(key,{})
  for r in a['revisions']:
   h[r['revid']]={'page_id':a['page_id'],'title':a['title'],'rev_id':r['revid'],'timestamp':r['timestamp'],'text':r['slots']['main']['*']}
 cur.execute("SET time_zone='+00:00'");cur.execute('SET system_versioning_insert_history=1')
 # This importer only runs on the dedicated npov schema, never another service.
 cur.execute('SELECT COUNT(*) AS n FROM revision FOR SYSTEM_TIME ALL')
 if cur.fetchone()['n']==0:
  for (lang,pid),versions in history.items():
   vs=sorted(versions.values(),key=lambda r:str(r['timestamp']))
   for i,r in enumerate(vs):
    ts=str(r['timestamp']).replace('T',' ').replace('Z','').replace('+00:00','')
    end=str(vs[i+1]['timestamp']).replace('T',' ').replace('Z','').replace('+00:00','') if i+1<len(vs) else None
    if r.get('archive') and (not end or end>'2026-10-01 00:00:00'):
     end='2026-10-01 00:00:00' # Archive coverage stops here; do not bridge missing revisions.
    if end==ts:continue # same-second older edit has zero validity interval, not a fabricated time
    vals=(lang,pid,r['rev_id'],r['title'],r['text'],ts)
    if end:cur.execute('INSERT INTO revision (lang,page_id,rev_id,title,text,row_start,row_end) VALUES (%s,%s,%s,%s,%s,%s,%s)',vals+(end,))
    else:cur.execute('INSERT INTO revision (lang,page_id,rev_id,title,text,row_start) VALUES (%s,%s,%s,%s,%s,%s)',vals)
 print('History loaded',flush=True)
 article_output=[];query_times=[]
 for q in QIDS:
  group=[a for a in articles if a['wikidata_id']==q];fi=next(a for a in group if a['lang']=='fi');ens=next(a for a in group if a['lang']=='en')
  findings=[];distances=[]
  for p,v in zip(passages,emb):
   if p['qid']!=q or p['lang']!='fi':continue
   matches={};flags=[]
   for lang in ['en','sv']:
    t=time.perf_counter();cur.execute(ALIGN_SQL,(json.dumps(v.tolist()),q,lang));rs=cur.fetchall();query_times.append((time.perf_counter()-t)*1000)
    if not rs:continue
    m=rs[0];sim=1-float(m['distance']);distances.append(float(m['distance']));verdict=check(p['text'],m['text'],sim)
    matches[lang]={**m,'distance':float(m['distance']),'check':verdict,'alternatives':[{**x,'distance':float(x['distance'])} for x in rs[1:]]}
    if verdict['kind'] not in ['aligned','emphasis']:flags.append(verdict['kind'])
   item={'id':p['id'],'qid':q,'fi':p,'matches':matches,'flags':flags,'tone':tone(p['text']),'source':source_state(p['text'])}
   findings.append(item)
   cur.execute('REPLACE INTO finding VALUES (%s,%s,%s)',(p['id'],q,json.dumps(item,ensure_ascii=False)))
  findings.sort(key=lambda f:(-sum(x in ['date-review','numeric-review'] for x in f['flags']),-bool(f['tone']),f['fi']['ordinal']))
  distance=float(np.mean(distances)) if distances else 1
  reviews=sum(any(x in ['date-review','numeric-review'] for x in f['flags']) for f in findings)
  coverage=sum('coverage' in f['flags'] for f in findings)
  article_output.append({'qid':q,'title':ens['title'],'fi_title':fi['title'],'distance':distance,'review_count':reviews,'coverage_count':coverage,'passage_count':len(findings),'versions':[{k:a[k] for k in ['lang','page_id','rev_id','title','date_modified','origin']} for a in group],'findings':findings})
 article_output.sort(key=lambda a:(-a['review_count'],-a['distance']))
 cur.execute('SELECT COUNT(*) AS n FROM revision FOR SYSTEM_TIME ALL');nrev=cur.fetchone()['n']
 cur.execute('SELECT VERSION() AS version');version=cur.fetchone()['version']
 output={'built_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'articles':article_output,'database':{'version':version,'passages':len(passages),'revisions':nrev,'topics':len(QIDS),'model':'paraphrase-multilingual-MiniLM-L12-v2','dimensions':384,'max_tokens':128,'query_p50_ms':float(np.median(query_times)),'query_p95_ms':float(np.percentile(query_times,95)),'query_count':len(query_times)},'sql':{'alignment':ALIGN_SQL}}
 json.dump(output,open(ROOT/'public/snapshot.json','w'),ensure_ascii=False)
 json.dump(output['database'],open(ROOT/'eval/database-run.json','w'),indent=2)
 print(json.dumps(output['database']),flush=True)
if __name__=='__main__':main()
