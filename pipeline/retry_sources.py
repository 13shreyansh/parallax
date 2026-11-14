"""Job 03 source recovery: availability API first, then metered Context.dev."""
import json,time,threading,concurrent.futures,re,os,urllib.parse
import requests,numpy as np
from .common import WORK,ROOT,UA,db,credentials,digest,now
from .sources import read_url,chunks,book_preview
from .ingest import encoder

LOCK=threading.Lock()
LEDGER=WORK/'context-credit-ledger.json'

def acceptable(text):
    if not text or len(text.strip())<250:return False
    return not re.search(r'^(?:#\s*)?(?:access denied|just a moment|page not found|404\b|client challenge|site (?:is )?under construction|verify you are human|cookie consent)',text.strip(),re.I)

def archive(source):
    path=WORK/'source-retries';path.mkdir(exist_ok=True)
    cache=path/f'{source["id"]}-archive.json'
    if cache.exists():return json.loads(cache.read_text())
    s=dict(source);s['archive_attempted_at']=now()
    try:
        r=requests.get('https://archive.org/wayback/available',params={'url':s['url']},headers={'User-Agent':UA},timeout=(6,20));snap=r.json().get('archived_snapshots',{}).get('closest',{})
        if snap.get('available'):
            u=snap['url'].replace('http://','https://',1);s['available_archive_url']=u;got=read_url(u)
            if got and acceptable(got['text']):s.update(got,status='Read',archive_url=u,retrieval_method='Internet Archive availability API')
    except Exception:pass
    cache.write_text(json.dumps(s,ensure_ascii=False,default=str));return s

def scrape(source):
    path=WORK/'source-retries'/f'{source["id"]}-context.json'
    if path.exists():return json.loads(path.read_text())
    s=dict(source)
    with LOCK:
        ledger=json.loads(LEDGER.read_text()) if LEDGER.exists() else {'limit':3000,'reserved':0,'spent':0,'calls':[]}
        # Standard Markdown with PDF OCR explicitly off costs one credit. Reserve five anyway.
        if ledger['reserved']+5>3000:return s
        ledger['reserved']+=5;LEDGER.write_text(json.dumps(ledger,indent=2))
    key=os.environ['CONTEXT_DEV_API_KEY']
    try:
        r=requests.post('https://api.context.dev/v1/web/scrape',headers={'Authorization':'Bearer '+key},json={'url':s['url'],'formats':{'markdown':True},'sharedParams':{'mainContentOnly':True,'parsers':{'pdf':{'ocr':'off'}}},'tags':['parallax-job03']},timeout=120)
        result=r.json();credit=float(result.get('key_metadata',{}).get('credits_consumed',0));md=result.get('markdown',{})
        with LOCK:
            ledger=json.loads(LEDGER.read_text());ledger['spent']+=credit;ledger['calls'].append({'source_id':s['id'],'status':r.status_code,'credits':credit,'request_id':result.get('request_id'),'at':now()});LEDGER.write_text(json.dumps(ledger,indent=2))
        if r.ok and md.get('success') and acceptable(md.get('data')):
            final=result.get('metadata',{}).get('finalUrl') or result.get('url') or s['url'];original=urllib.parse.urlsplit(s['url']);resolved=urllib.parse.urlsplit(final)
            if not (original.path not in ['', '/'] and resolved.path in ['', '/']):
                s.update(text=md['data'],title=result.get('metadata',{}).get('title') or s.get('title'),status='Read',final_url=final,retrieval_method='Context.dev scrape',context_request_id=result.get('request_id'))
        # Never store headers, tokens, account profiles or other account metadata.
    except Exception:pass
    if book_preview(s['url']):s['status']='Book, not checked'
    path.write_text(json.dumps(s,ensure_ascii=False,default=str));return s

def main():
    os.environ['CONTEXT_DEV_API_KEY']=credentials(ROOT.parent/'hostinger/.env')['CONTEXT_DEV_API_KEY']
    c=db();cur=c.cursor();cur.execute("SELECT DISTINCT s.* FROM cited_source s JOIN claim_source cs ON cs.source_id=s.id JOIN claim cl ON cl.id=cs.claim_id WHERE s.status='Source unreachable' AND s.url IS NOT NULL");rows=cur.fetchall();c.close();print('Unreachable URLs to retry',len(rows),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:recovered=list(pool.map(archive,rows))
    pending=[s for s in recovered if s['status']!='Read'];print('Archive recovered',len(rows)-len(pending),'; Context remaining',len(pending),flush=True)
    model=encoder();c=db();cur=c.cursor()
    def store(s):
        if s['status']!='Read':return
        s['read_at']=now();s['content_sha256']=digest(s['text'])
        (WORK/'sources'/f'{s["id"]}.json').write_text(json.dumps(s,ensure_ascii=False,default=str))
        cur.execute('UPDATE cited_source SET title=%s,status=%s,text=%s,archive_url=%s,read_at=UTC_TIMESTAMP(),content_sha256=%s,metadata=%s WHERE id=%s',(s['title'],s['status'],s['text'],s.get('archive_url'),s['content_sha256'],json.dumps({'retrieval_method':s.get('retrieval_method'),'context_request_id':s.get('context_request_id'),'final_url':s.get('final_url')}),s['id']))
        texts=chunks(s['text']);vs=model.encode(texts,batch_size=64,normalize_embeddings=True,show_progress_bar=False)
        cur.executemany('REPLACE INTO source_chunk VALUES (%s,%s,%s,%s,%s)',[(digest([s['id'],i,t])[:32],s['id'],i,t,np.asarray(v,dtype='<f4').tobytes()) for i,(t,v) in enumerate(zip(texts,vs))])
        print('Recovered',s['id'],s.get('retrieval_method'),len(s['text']),'characters',flush=True)
    for s in recovered:
        if s['status']=='Read':store(s)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(scrape,s) for s in pending]
        for future in concurrent.futures.as_completed(futures):store(future.result())
    cur.execute("SELECT s.status,COUNT(DISTINCT s.id) n FROM cited_source s JOIN claim_source cs ON cs.source_id=s.id JOIN claim cl ON cl.id=cs.claim_id WHERE cl.qid='Q134949' AND s.url IS NOT NULL GROUP BY s.status")
    (WORK/'job03-source-after.json').write_text(json.dumps({'at':now(),'counts':cur.fetchall(),'context':json.loads(LEDGER.read_text()) if LEDGER.exists() else {'spent':0}},indent=2));c.close()

if __name__=='__main__':main()
