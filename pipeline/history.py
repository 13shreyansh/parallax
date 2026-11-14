"""Genuine revision import, including complete available fi archive and API continuation."""
import gzip,json,datetime,argparse,concurrent.futures,re,html
import pyarrow.parquet as pq
from .common import ROOT,WORK,db,wiki,now

def cache_api_history(article):
    directory=WORK/'history'/f'{article["lang"]}-{article["page_id"]}';directory.mkdir(parents=True,exist_ok=True)
    state=directory/'state.json'
    s=json.loads(state.read_text()) if state.exists() else {'continue':{},'page':0,'complete':False}
    if s['complete']:return
    while True:
        params={'action':'query','pageids':article['page_id'],'prop':'revisions','rvprop':'ids|timestamp|content|comment','rvslots':'main','rvlimit':50,'rvdir':'newer',**s['continue']}
        if article['lang']=='fi':params['rvstart']='2026-10-01T00:00:00Z'
        j=wiki(article['lang'],params)
        with gzip.open(directory/f'{s["page"]:05d}.json.gz','wt',encoding='utf-8') as f:json.dump(j,f,ensure_ascii=False)
        s={'continue':j.get('continue',{}),'page':s['page']+1,'complete':'continue' not in j}
        state.write_text(json.dumps(s))
        print('history',article['lang'],s['page']*50,'revisions fetched',flush=True)
        if s['complete']:return

def revisions(article):
    vs={}
    if article['lang']=='fi':
        for p in sorted((ROOT/'work/official/m').glob('versions-*.parquet')):
            for r in pq.read_table(p,filters=[('page_id','=',article['page_id'])],columns=['rev_id','timestamp','text','comment']).to_pylist():
                vs[r['rev_id']]={'rev_id':r['rev_id'],'timestamp':str(r['timestamp']).replace('+00:00','Z'),'text':r['text'],'comment':r['comment']}
    for p in sorted((WORK/'history'/f'{article["lang"]}-{article["page_id"]}').glob('*.gz')):
        with gzip.open(p,'rt') as f:j=json.load(f)
        for page in j['query']['pages']:
            for r in page.get('revisions',[]):
                if 'content' not in r.get('slots',{}).get('main',{}):continue
                vs[r['revid']]={'rev_id':r['revid'],'timestamp':r['timestamp'],'text':r['slots']['main']['content'],'comment':r.get('comment','')}
    return sorted(vs.values(),key=lambda r:(r['timestamp'],r['rev_id']))

def load_history(article):
    c=db();cur=c.cursor();key=f'history-{article["lang"]}-{article["page_id"]}'
    cur.execute('SELECT state FROM ingestion_log WHERE id=%s',(key,))
    if (cur.fetchone() or {}).get('state')=='complete':c.close();return
    versions=revisions(article)
    cur.execute("SET system_versioning_insert_history=1")
    for i,r in enumerate(versions):
        start=r['timestamp'].replace('T',' ').removesuffix('Z')
        end=versions[i+1]['timestamp'].replace('T',' ').removesuffix('Z') if i+1<len(versions) else None
        if start==end:continue
        fields=('lang','page_id','qid','rev_id','title','text','comment','row_start')
        values=(article['lang'],article['page_id'],article['qid'],r['rev_id'],article['title'],r['text'],r['comment'],start)
        if end:fields+=('row_end',);values+=(end,)
        cur.execute('INSERT INTO revision ('+','.join(fields)+') VALUES ('+','.join(['%s']*len(values))+')',values)
    cur.execute('REPLACE INTO ingestion_log VALUES (%s,%s,UTC_TIMESTAMP(),%s)',(key,'complete',json.dumps({'revisions':len(versions),'provenance':'Sponsor M fi archive plus complete API history; missing/hidden revisions cannot be recovered'})))
    c.close();print('history loaded',article['lang'],len(versions),flush=True)

def normalize(text):
    text=re.sub(r'<!--.*?-->',' ',text,flags=re.S)
    text=re.sub(r'<ref\b[^>]*?/\s*>|<ref\b[^>]*>.*?</ref\s*>',' ',text,flags=re.I|re.S)
    def template(m):
        parts=m.group()[2:-2].split('|');name=parts[0].strip().lower()
        if name in ('convert','cvt','val','num'):return ' '.join(parts[1:3])
        if name in ('nowrap','nobr','small','lang','lang-fi','lang-sv','lang-en'):return parts[-1]
        if name in ('snd','spaced ndash','ndash'):return '–'
        return ' '
    for _ in range(15):
        updated=re.sub(r'\{\{[^{}]*\}\}',template,text)
        if updated==text:break
        text=updated
    text=re.sub(r'\[\[(?:[^\]|]+\|)?([^\]]+)\]\]',r'\1',text)
    text=re.sub(r"'{2,}",'',text)
    text=re.sub(r'<[^>]+>',' ',text)
    text=re.sub(r'\s+',' ',html.unescape(text)).strip()
    return text

def onset(qid):
    c=db();cur=c.cursor();cur.execute("SELECT * FROM flag WHERE qid=%s AND id NOT IN (SELECT flag_id FROM quality_exclusion) AND JSON_EXTRACT(payload,'$.current_confirmed')=true",(qid,));flags=cur.fetchall()
    cur.execute('SELECT * FROM article WHERE qid=%s',(qid,));articles={a['lang']:a for a in cur.fetchall()}
    bylang={}
    for row in flags:
        f=json.loads(row['payload']);lang=f['language']
        if not set(f.get('marks',{})).issubset({v.get('claim_id') for v in f.get('versions',{}).values()}):continue
        if f['check']=='src':
            cur.execute("SELECT status FROM cited_source WHERE id=%s",(f.get('source_id'),))
            if (cur.fetchone() or {}).get('status')!='Read':continue
        if lang not in bylang:
            cur.execute('SELECT * FROM article WHERE qid=%s AND lang=%s',(qid,lang));a=cur.fetchone();vs=revisions(a);bylang[lang]=(a,vs,[normalize(r['text']) for r in vs])
        a,vs,normalized=bylang[lang]
        quote=f['versions'].get(lang,{}).get('text','')
        if not quote:continue
        needle=normalize(quote)
        found=[]
        for i,text in enumerate(normalized):
            if needle in text:found.append(i)
        if not found:continue
        first=found[0];prev=vs[first-1] if first else None;r=vs[first]
        # State an exact-wording onset only, never pretend this proves the underlying idea's first appearance.
        history={'entered_at':r['timestamp'],'entered_revision':r['rev_id'],'parent_revision':prev['rev_id'] if prev else None,'entry_scope':'First stored appearance of this exact claim wording','complete_available_history':True,'ever_supported':'Not established. Historical source contents were not reconstructed.','changes':[{'date':r['timestamp'],'revision':r['rev_id'],'label':'wording added','comment':r.get('comment','')}]}
        if prev:
            history['before_revision']=prev['rev_id'];history['before_at']=prev['timestamp'];history['before_absent']=True
        last_seen=True
        for i in range(first+1,len(vs)):
            present=i in found
            if present!=last_seen and len(history['changes'])<4:history['changes'].append({'date':vs[i]['timestamp'],'revision':vs[i]['rev_id'],'label':'wording added' if present else 'wording changed','comment':vs[i].get('comment','')})
            last_seen=present
        f['history']=history
        from .notes import fill_note
        fill_note(f,articles)
        # A flag enters the product only with two judges, literal evidence, and a proven stored boundary.
        cur.execute('UPDATE flag SET payload=%s,shown=1 WHERE id=%s',(json.dumps(f,ensure_ascii=False),f['id']))
    c.close()

def main():
    p=argparse.ArgumentParser();p.add_argument('--qid',default='Q134949');p.add_argument('--onset-only',action='store_true');args=p.parse_args()
    c=db();cur=c.cursor();cur.execute('SELECT * FROM article WHERE qid=%s',(args.qid,));articles=cur.fetchall();c.close()
    if not args.onset_only:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(cache_api_history,articles))
        for a in articles:load_history(a)
    onset(args.qid)

if __name__=='__main__':main()
