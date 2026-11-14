"""Probe a bounded L subset. This is a load/query test, not a full-scale claim."""
import sys,pathlib,json,time
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pyarrow.parquet as pq,numpy as np
from sentence_transformers import SentenceTransformer
from server.db import connect
f=pq.ParquetFile(ROOT/'work/official/l/articles-fi.parquet');rows=[]
for b in f.iter_batches(batch_size=1000,columns=['page_id','title','text']):rows=b.to_pylist();break
model=SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',cache_folder=str(ROOT/'work/models'),device='mps')
t=time.perf_counter();emb=model.encode([(r['title']+'. '+r['text'][:400]) for r in rows],normalize_embeddings=True,batch_size=64,show_progress_bar=False);embedding_s=time.perf_counter()-t
con=connect();c=con.cursor();c.execute('CREATE TABLE IF NOT EXISTS scale_probe(page_id INT PRIMARY KEY,title VARCHAR(255),embedding VECTOR(384) NOT NULL,VECTOR INDEX(embedding) M=16 DISTANCE=cosine)')
t=time.perf_counter()
for r,v in zip(rows,emb):c.execute('REPLACE INTO scale_probe VALUES(%s,%s,%s)',(r['page_id'],r['title'],np.asarray(v,dtype='<f4').tobytes()))
load_s=time.perf_counter()-t;timings=[]
for v in emb[:30]:
 t=time.perf_counter();c.execute('SELECT page_id,VEC_DISTANCE_COSINE(embedding,VEC_FromText(%s)) AS distance FROM scale_probe ORDER BY distance LIMIT 5',(json.dumps(v.tolist()),));c.fetchall();timings.append((time.perf_counter()-t)*1000)
result={'L_file_rows':f.metadata.num_rows,'L_loaded_vector_rows':len(rows),'L_selection':'First 1000 rows in official Parquet order, title + first 400 characters. Not representative sampling.','embedding_seconds':embedding_s,'load_seconds':load_s,'queries':len(timings),'p50_ms':float(np.median(timings)),'p95_ms':float(np.percentile(timings,95)),'M_file_rows':sum(pq.read_metadata(p).num_rows for p in (ROOT/'work/official/m').glob('*.parquet')),'M_loaded_revision_rows':12944,'limits':'Bounded schema/ingestion/query probe only. Full L or M database load, concurrent traffic and multilingual quality at full scale unmeasured.'}
json.dump(result,open(ROOT/'eval/scale-results.json','w'),indent=2);print(json.dumps(result))
