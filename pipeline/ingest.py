import json,concurrent.futures,argparse
import numpy as np
from collections import Counter
from sentence_transformers import SentenceTransformer
from .common import WORK,ROOT,db,digest,now
from .extract import split_claims
from .sources import fetch_source,chunks

MODEL='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
EXTRACT_VERSION='v2'
def encoder(device='mps'):
    return SentenceTransformer(MODEL,cache_folder=str(ROOT/'work/models'),device=device)

def ingest(qid=None,source_workers=12,theme=None,claims_only=False):
    c=db();cur=c.cursor();model=encoder();articles=[];claims=[]
    theme_qids=None
    if theme:
        cur.execute('SELECT qid FROM topic_theme WHERE theme=%s',(theme,));theme_qids={r['qid'] for r in cur.fetchall()}
    for p in sorted((WORK/'articles').glob('*.json')):
        a=json.loads(p.read_text())
        if qid and a['qid']!=qid:continue
        if theme_qids is not None and a['qid'] not in theme_qids:continue
        cur.execute('SELECT rev_id FROM article WHERE qid=%s AND lang=%s',(a['qid'],a['lang']));old=cur.fetchone()
        marker=f'claims-{EXTRACT_VERSION}-{a["lang"]}-{a["page_id"]}-{a["rev_id"]}'
        cur.execute('SELECT state FROM ingestion_log WHERE id=%s',(marker,));complete=cur.fetchone()
        if old and old['rev_id']==a['rev_id'] and complete and complete['state']=='complete':continue
        articles.append(a)
        cur.execute('REPLACE INTO article VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(a['qid'],a['lang'],a['page_id'],a['rev_id'],a['title'],a['revised_at'].replace('T',' ').replace('Z',''),a['wikitext'],a['origin']))
        claims+=split_claims(a)
        if len(articles)%100==0:print('parsed',len(articles),'versions;',len(claims),'claims',flush=True)
    print('Embedding',len(claims),'claims in',len(articles),'versions',flush=True)
    if claims:
        vectors=model.encode([x['text'] for x in claims],batch_size=64,normalize_embeddings=True,show_progress_bar=False)
        for cl,v in zip(claims,vectors):
            cur.execute('REPLACE INTO claim VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(cl['id'],cl['qid'],cl['lang'],cl['rev_id'],cl['ordinal'],cl['section'],cl['text'],json.dumps(cl['citations'],ensure_ascii=False),None,np.asarray(v,dtype='<f4').tobytes()))
        totals=Counter((cl['qid'],cl['lang']) for cl in claims)
        for a in articles:
            cur.execute('REPLACE INTO ingestion_log VALUES (%s,%s,UTC_TIMESTAMP(),%s)',(f'claims-{EXTRACT_VERSION}-{a["lang"]}-{a["page_id"]}-{a["rev_id"]}','complete',json.dumps({'claims':totals[(a['qid'],a['lang'])]})))
    if claims_only:c.close();return
    # Resume all pending source references, even if their article already exists.
    cur.execute('SELECT id,citations FROM claim'+(' WHERE qid=%s' if qid else ''),(qid,) if qid else ())
    refs=cur.fetchall();urls={};offline={}
    for row in refs:
        for ref in json.loads(row['citations']):
            if ref['urls']:
                for u in ref['urls']:urls.setdefault(u,[]).append(row['id'])
            else:offline.setdefault(ref['id'],{'ref':ref,'claims':[]})['claims'].append(row['id'])
    for sid,o in offline.items():
        ref=o['ref'];cur.execute('INSERT IGNORE INTO cited_source(id,title,status,metadata) VALUES (%s,%s,%s,%s)',(sid,ref['metadata'].get('title') or ref['metadata'].get('teos') or ref['label'] or 'Book reference','Book, not checked',json.dumps(ref)))
        cur.executemany('INSERT IGNORE INTO claim_source VALUES (%s,%s)',[(cid,sid) for cid in o['claims']])
    print('Fetching',len(urls),'distinct citation URLs;',len(offline),'offline references',flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=source_workers) as pool:
        for i,s in enumerate(pool.map(fetch_source,urls)):
            cur.execute('SELECT id,content_sha256 FROM cited_source WHERE id=%s',(s['id'],));exists=cur.fetchone()
            cur.execute('REPLACE INTO cited_source VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(s['id'],s['url'],s['title'],s['status'],s.get('archive_url'),s['text'],s['read_at'].replace('T',' ').replace('Z',''),s.get('content_sha256'),json.dumps({'final_url':s.get('final_url')})))
            cur.executemany('INSERT IGNORE INTO claim_source VALUES (%s,%s)',[(cid,s['id']) for cid in urls[s['url']]])
            if s['status']=='Read' and (not exists or exists['content_sha256']!=s.get('content_sha256')):
                if exists:cur.execute('DELETE FROM source_chunk WHERE source_id=%s',(s['id'],))
                texts=chunks(s['text']);vs=model.encode(texts,batch_size=64,normalize_embeddings=True,show_progress_bar=False)
                cur.executemany('REPLACE INTO source_chunk VALUES (%s,%s,%s,%s,%s)',[(digest([s['id'],i,t])[:32],s['id'],i,t,np.asarray(v,dtype='<f4').tobytes()) for i,(t,v) in enumerate(zip(texts,vs))])
            print('source',i+1,'/',len(urls),s['status'],flush=True)
    for a in articles:
        cur.execute("UPDATE topic SET state='ingested',last_changed=(SELECT MAX(revised_at) FROM article WHERE qid=%s) WHERE qid=%s",(a['qid'],a['qid']))
    c.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--qid');p.add_argument('--theme');p.add_argument('--claims-only',action='store_true');args=p.parse_args();ingest(args.qid,theme=args.theme,claims_only=args.claims_only)
