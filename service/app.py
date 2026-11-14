"""Parallax's database-backed API. No snapshots or local fallback in the product."""
import os,json,time,datetime,re,hmac,threading
from collections import defaultdict,deque
from flask import Flask,request,jsonify,send_from_directory
from pipeline.common import db,ROOT
from pipeline.check import ALIGN_SQL,SOURCE_SQL
from pipeline.text import normalize,HistoricalIndex

app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH']=4096
_encoder=None;_encoder_lock=threading.Lock();_limits=defaultdict(deque)

def unpack(value):return json.loads(value) if isinstance(value,str) else value

def run(cur,sql,args=(),traces=None,label=None):
    t=time.perf_counter();cur.execute(sql,args);rows=cur.fetchall()
    if traces is not None:traces.append({'name':label,'sql':cur.mogrify(sql,args),'rows':len(rows),'ms':round((time.perf_counter()-t)*1000,2)})
    return rows

def counts(cur):
    sql="""SELECT (SELECT COUNT(DISTINCT qid) FROM claim) articles,(SELECT COUNT(*) FROM article WHERE qid IN (SELECT DISTINCT qid FROM claim)) versions,(SELECT COUNT(*) FROM claim) claims,(SELECT COUNT(DISTINCT s.id) FROM cited_source s JOIN claim_source cs ON cs.source_id=s.id JOIN claim cl ON cl.id=cs.claim_id) sources,(SELECT COUNT(DISTINCT s.id) FROM cited_source s JOIN claim_source cs ON cs.source_id=s.id JOIN claim cl ON cl.id=cs.claim_id WHERE s.status='Read') sources_read,(SELECT COUNT(*) FROM revision FOR SYSTEM_TIME ALL) revisions,(SELECT COUNT(*) FROM published_flag f LEFT JOIN editor_reviews r ON r.flag_id=f.id WHERE f.shown=1 AND COALESCE(r.dismissed,0)=0) flags,(SELECT COUNT(*) FROM editor_reviews WHERE dismissed=1) dismissed,(SELECT COALESCE(SUM(copies),0) FROM note_copies) copied,(SELECT MAX(checked_at) FROM flag) updated_at"""
    return run(cur,sql)[0]

def flag_rows(cur,qid=None):
    rows=run(cur,"SELECT f.*,r.reason,r.dismissed,r.reviewed_at,COALESCE(n.copies,0) copied_count FROM published_flag f LEFT JOIN claim_group g ON g.id=f.group_id LEFT JOIN editor_reviews r ON r.flag_id=f.id LEFT JOIN note_copies n ON n.flag_id=f.id WHERE f.shown=1"+(' AND f.qid=%s' if qid else '')+" ORDER BY g.ordinal,FIELD(f.check_type,'src','lang','tone','fact'),f.id",(qid,) if qid else ())
    return [{**unpack(r['payload']),'dismissed':bool(r['dismissed']),'review_reason':r['reason'],'reviewed_at':r['reviewed_at'],'copied_count':r['copied_count']} for r in rows]

def article_meta(cur,qid):
    rows=run(cur,'SELECT * FROM topic WHERE qid=%s',(qid,))
    if not rows:return None
    a=rows[0];a['titles']=unpack(a['titles']);a['versions']=run(cur,'SELECT lang,title,page_id,rev_id,revised_at FROM article WHERE qid=%s ORDER BY FIELD(lang,\'fi\',\'sv\',\'en\',\'de\',\'ru\')',(qid,));return a

def temporal_query(versions,instant):
    # The system-versioned primary key is (lang,page_id,row_end). Looking up qid
    # alone reads every historical article body; these branches seek one version.
    part='SELECT lang,page_id,rev_id,title,text,row_start revised_at FROM revision FOR SYSTEM_TIME AS OF TIMESTAMP %s FORCE INDEX(history_at) WHERE lang=%s AND page_id=%s'
    return ' UNION ALL '.join(part for _ in versions),tuple(value for v in versions for value in (instant,v['lang'],v['page_id']))

@app.before_request
def access():
    token=os.environ.get('PARALLAX_BRIDGE_TOKEN')
    public=request.path in ['/','/ask','/method','/favicon.svg','/api/parallax'] or request.path.startswith(('/a/','/assets/','/fonts/'))
    if token and not public and not hmac.compare_digest(request.headers.get('X-Parallax-Token',''),token):return jsonify(error='Access denied'),403
    if request.method=='POST':
        if request.content_type!='application/json':return jsonify(error='Use JSON'),415
        ip=request.headers.get('X-Parallax-Client','unknown');q=_limits[ip];now=time.monotonic()
        while q and q[0]<now-60:q.popleft()
        if len(q)>=30:return jsonify(error='Too many changes. Try again in a minute.'),429
        q.append(now)

@app.errorhandler(Exception)
def error(e):
    # Never return connection details, prompts, credentials or a traceback.
    from werkzeug.exceptions import HTTPException
    if isinstance(e,HTTPException):return jsonify(error='This page could not be found.'),e.code
    app.logger.error('Parallax request failed: %s',type(e).__name__)
    return jsonify(error='The database did not answer. Try again in a moment.'),503

@app.after_request
def security(response):
    response.headers['X-Content-Type-Options']='nosniff';response.headers['X-Frame-Options']='DENY'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    response.headers['Cache-Control']='public,max-age=31536000,immutable' if request.path.startswith(('/assets/','/fonts/')) else 'no-store'
    return response

@app.get('/')
@app.get('/a/<qid>')
@app.get('/ask')
@app.get('/method')
def frontend(qid=None):return send_from_directory(ROOT/'frontend','index.html')

@app.get('/assets/<path:name>')
def asset(name):return send_from_directory(ROOT/'frontend/assets',name)

@app.get('/fonts/<path:name>')
def font(name):return send_from_directory(ROOT/'frontend/fonts',name)

@app.get('/favicon.svg')
def favicon():return send_from_directory(ROOT/'frontend','favicon.svg')

@app.route('/api/parallax',methods=['GET','POST'])
def browser_api():
    mode=request.args.get('mode','home')
    allowed={'GET':{'health','home','article','search','method'},'POST':{'review','copied'}}
    if mode not in allowed[request.method]:return jsonify(error='This action is not available.'),405
    return app.view_functions[mode]()

@app.get('/health')
def health():
    c=db();cur=c.cursor();v=run(cur,'SELECT VERSION() version')[0]['version'];c.close()
    return jsonify(ok=True,database=v,commit=os.environ.get('PARALLAX_COMMIT','local'))

@app.get('/home')
def home():
    c=db();cur=c.cursor();traces=[];theme=request.args.get('theme','finland-second-world-war');sort=request.args.get('sort','distance')
    themes=run(cur,"SELECT t.*,COUNT(tt.qid) articles FROM theme t JOIN topic_theme tt ON tt.theme=t.slug WHERE t.slug='finland-second-world-war' GROUP BY t.slug,t.title")
    order='issues DESC,t.distance DESC' if sort=='issues' else 't.distance DESC,issues DESC'
    rows=run(cur,"""SELECT t.qid,t.title,t.titles,t.distance,t.last_changed,t.state,COUNT(CASE WHEN f.shown=1 AND COALESCE(r.dismissed,0)=0 THEN 1 END) issues,
    SUM(CASE WHEN f.check_type='src' AND f.shown=1 AND COALESCE(r.dismissed,0)=0 THEN 1 ELSE 0 END) src,
    SUM(CASE WHEN f.check_type='lang' AND f.shown=1 AND COALESCE(r.dismissed,0)=0 THEN 1 ELSE 0 END) lang,
    SUM(CASE WHEN f.check_type='tone' AND f.shown=1 AND COALESCE(r.dismissed,0)=0 THEN 1 ELSE 0 END) tone,
    SUM(CASE WHEN f.check_type='fact' AND f.shown=1 AND COALESCE(r.dismissed,0)=0 THEN 1 ELSE 0 END) fact
    FROM topic t JOIN topic_theme tt ON tt.qid=t.qid LEFT JOIN published_flag f ON f.qid=t.qid LEFT JOIN editor_reviews r ON r.flag_id=f.id
    WHERE tt.theme=%s AND t.distance IS NOT NULL GROUP BY t.qid ORDER BY """+order,(theme,),traces,'Ranked articles')
    for r in rows:r['titles']=unpack(r['titles'])
    qids={r['qid']:i for i,r in enumerate(rows)};fs=[f for f in flag_rows(cur) if f['qid'] in qids and not f['dismissed'] and f.get('source') and f['check'] in ['src','fact','lang'] and len(f['source'].get('passage',''))<=220 and all(len(v['text'])<=220 for v in ([f['versions'][f['language']]] if f['check']=='src' else f.get('versions',{}).values()))]
    fs.sort(key=lambda f:(0 if f['check']=='src' and f['verdict']=='Contradicted' else 1 if f['check']=='fact' else 2,qids[f['qid']]))
    result={'themes':themes,'theme':theme,'sort':sort,'articles':rows[:10],'example':fs[0] if fs else None,'counts':counts(cur),'queries':traces};c.close();return jsonify(result)

@app.get('/article')
def article():
    qid=request.args.get('qid','');asof=request.args.get('asof');c=db();cur=c.cursor();traces=[];a=article_meta(cur,qid)
    if not a:c.close();return jsonify(error='This article is not in the database.'),404
    fs=flag_rows(cur,qid);selected=next((f for f in fs if f['id']==request.args.get('flag')),None) or next((f for f in fs if not f['dismissed']),None)
    gs=run(cur,'SELECT * FROM claim_group WHERE qid=%s ORDER BY ordinal',(qid,))
    groups=[{**g,'versions':unpack(g['versions']),'checks':unpack(g['checks'])} for g in gs]
    for g in groups:g['flags']=[f['id'] for f in fs if f['group_id']==g['id']]
    # Actually run the three inspection queries for the current selected claim.
    anchor=selected['claim_id'] if selected else groups[0]['anchor_id'] if groups else None
    if anchor:
        run(cur,ALIGN_SQL,(anchor,qid,'sv'),traces,'Aligned claims')
        run(cur,SOURCE_SQL,(anchor,anchor),traces,'Closest source passage')
    date=None
    if asof:
        try:date=datetime.date.fromisoformat(asof)
        except ValueError:c.close();return jsonify(error='Choose a valid date.'),400
        if date>datetime.datetime.now(datetime.timezone.utc).date():c.close();return jsonify(error='Choose today or an earlier date.'),400
    temporal_sql,temporal_args=temporal_query(a['versions'],(asof+' 23:59:59') if date else datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    past=run(cur,temporal_sql,temporal_args,traces,'As of '+(asof or 'today'))
    history=run(cur,'SELECT COUNT(*) revisions,MIN(row_start) earliest,MAX(row_start) latest FROM revision FOR SYSTEM_TIME ALL WHERE qid=%s',(qid,))[0]
    if date:
        versions={r['lang']:r for r in past}
        indexes={r['lang']:HistoricalIndex(r['text']) for r in past}
        for g in groups:
            for lang,v in g['versions'].items():
                r=versions.get(lang);passage=indexes[lang].match(v['text']) if r else None
                v['asof_present']=bool(passage);v['asof_text']=passage
                v['asof_match']='exact' if passage==normalize(v['text']) else 'similar' if passage else 'not found'
                v['asof_absence_verified']=any(f['claim_id']==v.get('claim_id',v.get('id')) and f.get('history',{}).get('material_absence_verified') and asof<str(f['history']['entered_at'])[:10] for f in fs)
                if r:v['asof_revision']=r['rev_id']
    unread=run(cur,"SELECT DISTINCT cl.id,cl.lang,LEFT(cl.text,80) text,s.title,s.url,s.status FROM claim cl JOIN claim_source cs ON cs.claim_id=cl.id JOIN cited_source s ON s.id=cs.source_id WHERE cl.qid=%s AND s.status<>'Read'",(qid,))
    a.update(flags=fs,groups=groups,history=history,queries=traces,unread=unread,asof=asof,claim_count=run(cur,'SELECT COUNT(*) n FROM claim WHERE qid=%s',(qid,))[0]['n'])
    c.close();return jsonify(a)

@app.get('/search')
def search():
    global _encoder
    question=request.args.get('q','').strip()
    if not question or len(question)>300:return jsonify(error='Ask a question up to 300 characters.'),400
    with _encoder_lock:
        if _encoder is None:
            from pipeline.embeddings import encoder
            _encoder=encoder(os.environ.get('PARALLAX_EMBED_DEVICE','cpu'))
        vec=_encoder.encode([question],normalize_embeddings=True,show_progress_bar=False)[0].tolist()
    c=db();cur=c.cursor();traces=[]
    sql="""SELECT 'claim' kind,id,qid,lang,section,text,VEC_DISTANCE_COSINE(embedding,VEC_FromText(%s)) distance FROM claim
    UNION ALL SELECT 'source' kind,sc.id,NULL qid,NULL lang,s.title section,sc.text,VEC_DISTANCE_COSINE(sc.embedding,VEC_FromText(%s)) distance FROM source_chunk sc JOIN cited_source s ON s.id=sc.source_id WHERE s.status='Read' ORDER BY distance LIMIT 18"""
    hits=run(cur,sql,(json.dumps(vec),json.dumps(vec)),traces,'Closest claims and source texts');best=next((h for h in hits if h['kind']=='claim'),None);group=None;flags=[];topic=None
    if best and best['distance']<=.7:
        gs=run(cur,'SELECT * FROM claim_group WHERE anchor_id=%s OR JSON_SEARCH(versions,\'one\',%s,NULL,\'$.*.claim_id\') IS NOT NULL LIMIT 1',(best['id'],best['id']))
        if gs:
            group={**gs[0],'versions':unpack(gs[0]['versions'])};flags=[f for f in flag_rows(cur,best['qid']) if f['group_id']==group['id'] and not f['dismissed']]
        else:group={'id':best['id'],'versions':{best['lang']:best}}
        topic=article_meta(cur,best['qid'])
    result={'question':question,'hits':hits,'group':group,'flags':flags,'topic':topic,'queries':traces,'counts':counts(cur)};c.close();return jsonify(result)

@app.get('/method')
def method():
    c=db();cur=c.cursor();fs=flag_rows(cur);examples={}
    for f in fs:
        if not f['dismissed'] and f['check'] not in examples:examples[f['check']]=f
    evaluations={r['name']:unpack(r['payload']) for r in run(cur,'SELECT * FROM evaluation')}
    result={'counts':counts(cur),'examples':examples,'evaluation':evaluations,'models':['gemini-3.8-flash','gemini-4-argon'],'database':run(cur,'SELECT VERSION() version')[0]['version']};c.close();return jsonify(result)

@app.post('/review')
def review():
    data=request.get_json();fid=data.get('flag_id');reason=data.get('reason');dismissed=data.get('dismissed',True)
    reasons=['A fair difference for this audience','The check misread the article or the source','Already fixed on Wikipedia']
    if not isinstance(dismissed,bool) or (dismissed and reason not in reasons):return jsonify(error='Choose one of the reasons.'),400
    # Production supplies a distinct account with INSERT/UPDATE only on review/copy tables.
    from service.writer import writer_db
    c=writer_db();cur=c.cursor()
    if not run(cur,'SELECT id FROM flag WHERE id=%s AND shown=1',(fid,)):c.close();return jsonify(error='This finding is not available.'),404
    cur.execute('INSERT INTO editor_reviews VALUES (%s,%s,%s,UTC_TIMESTAMP()) ON DUPLICATE KEY UPDATE reason=VALUES(reason),dismissed=VALUES(dismissed),reviewed_at=VALUES(reviewed_at)',(fid,reason if dismissed else None,dismissed))
    result=run(cur,'SELECT * FROM editor_reviews WHERE flag_id=%s',(fid,))[0];c.close();return jsonify(result)

@app.post('/copied')
def copied():
    from service.writer import writer_db
    c=writer_db();cur=c.cursor();fid=request.get_json().get('flag_id')
    if not run(cur,'SELECT id FROM flag WHERE id=%s AND shown=1',(fid,)):c.close();return jsonify(error='This finding is not available.'),404
    cur.execute('INSERT INTO note_copies VALUES (%s,1) ON DUPLICATE KEY UPDATE copies=copies+1',(fid,));n=run(cur,'SELECT copies FROM note_copies WHERE flag_id=%s',(fid,))[0];c.close();return jsonify(n)

if __name__=='__main__':
    from waitress import serve
    serve(app,host=os.environ.get('PARALLAX_BIND','127.0.0.1'),port=int(os.environ.get('PARALLAX_PORT','18808')),threads=8)
