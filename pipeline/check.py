"""Vector retrieval, cached independent model passes, and literal evidence gates."""
import json,time,argparse,concurrent.futures
from .common import db,digest,judge,FAST,STRONG,WORK,now
from .prompts import CHECK_PROMPT,RECHECK_PROMPT,RECALL_PROMPT,PRECISION_PROMPT,VERSION

ALIGN_SQL='''SELECT id,lang,section,text,rev_id,citations,VEC_DISTANCE_COSINE(embedding,(SELECT embedding FROM claim WHERE id=%s)) distance FROM claim WHERE qid=%s AND lang=%s ORDER BY distance LIMIT 3'''
SOURCE_SQL='''SELECT sc.id,sc.source_id,sc.text,VEC_DISTANCE_COSINE(sc.embedding,(SELECT embedding FROM claim WHERE id=%s)) distance FROM source_chunk sc JOIN claim_source cs ON cs.source_id=sc.source_id JOIN cited_source s ON s.id=sc.source_id WHERE cs.claim_id=%s AND s.status='Read' ORDER BY distance LIMIT 5'''

def attach_source(flag,payload):
    sid=flag.get('source_id');passage=flag.get('source_passage');source=payload['sources'].get(sid)
    if source and passage and passage in (source.get('full_source_text') or '\n'.join(p['text'] for p in source['passages'])):
        flag['source']={k:source[k] for k in ['id','title','url','archive_url','read_at']};flag['source']['passage']=passage
    elif flag.get('check')!='src':
        flag['source_id']=None;flag['source_passage']=None;flag['source_marks']=[]

def full_articles(qid):
    c=db();cur=c.cursor();cur.execute("SELECT lang,wikitext FROM article WHERE qid=%s AND lang IN ('fi','sv','en')",(qid,));out={r['lang']:r['wikitext'] for r in cur.fetchall()};c.close();return out

def build_groups(qid):
    c=db();cur=c.cursor();cur.execute('SELECT * FROM claim WHERE qid=%s ORDER BY FIELD(lang,\'en\',\'fi\',\'sv\',\'de\',\'ru\'),ordinal',(qid,));claims=cur.fetchall()
    claims=[x for x in claims if x['lang'] in ['fi','sv','en']]
    cur.execute("SELECT lang FROM article WHERE qid=%s AND lang IN ('fi','sv','en')",(qid,))
    languages=[r['lang'] for r in cur.fetchall()];seen=set();groups=[];distances=[]
    for anchor in claims:
        if anchor['lang']!='en' and anchor['id'] in seen:continue
        candidates={anchor['lang']:[anchor]}
        for lang in languages:
            if lang==anchor['lang']:continue
            cur.execute(ALIGN_SQL,(anchor['id'],qid,lang));rs=cur.fetchall()
            candidates[lang]=rs
            if rs:
                if anchor['lang'] in ['fi','sv','en'] and lang in ['fi','sv','en']:distances.append(min(1,max(0,float(rs[0]['distance']))))
                if float(rs[0]['distance'])<.32:seen.add(rs[0]['id'])
        groups.append({'id':digest([qid,anchor['id']])[:32],'qid':qid,'anchor_id':anchor['id'],'ordinal':len(groups),'candidates':candidates})
    if distances:cur.execute('UPDATE topic SET distance=%s WHERE qid=%s',(100*sum(distances)/len(distances),qid))
    c.close();return groups

def evidence(group,full=False):
    c=db();cur=c.cursor();out={'id':group['id'],'qid':group['qid'],'candidates':{},'sources':{}}
    candidates=dict(group['candidates'])
    if full and group['qid']=='Q134949':
        for lang in ['de','ru']:
            cur.execute(ALIGN_SQL,(group['anchor_id'],group['qid'],lang));candidates[lang]=cur.fetchall()
    for lang,rows in candidates.items():
        # Top three candidates are provided so models may reject a poor first pairing.
        out['candidates'][lang]=[]
        for row in rows:
            r={k:row[k] for k in ['id','lang','section','text','rev_id']}
            original_refs=json.loads(row.get('citations') or '[]')
            r['citation_context']=[{'scope':ref.get('citation_scope','sentence'),'paragraph':ref.get('paragraph_text'),'reference':ref.get('content')} for ref in original_refs]
            cur.execute('SELECT s.id,s.title,s.url,s.status FROM cited_source s JOIN claim_source cs ON s.id=cs.source_id WHERE cs.claim_id=%s',(row['id'],));r['citations']=cur.fetchall()
            cur.execute(SOURCE_SQL,(row['id'],row['id']));passages=cur.fetchall()
            for p in passages:
                sid=p['source_id']
                if sid not in out['sources']:
                    cur.execute('SELECT id,title,url,status,text,archive_url,read_at FROM cited_source WHERE id=%s',(sid,));s=cur.fetchone();s['read_at']=str(s['read_at'])
                    s['document_characters']=len(s['text'])
                    if full:s['full_source_text']=s['text']
                    del s['text'];s['passages']=[];out['sources'][sid]=s
                if p['id'] not in [x['id'] for x in out['sources'][sid]['passages']]:out['sources'][sid]['passages'].append({k:p[k] for k in ['id','text','distance']})
            out['candidates'][lang].append(r)
    # Absence requires the entire article, including infoboxes, never just failed retrieval.
    for lang,rows in group['candidates'].items():
        if (not rows or float(rows[0].get('distance',0))>.55) and lang in ['fi','sv','en']:
            cur.execute('SELECT wikitext FROM article WHERE qid=%s AND lang=%s',(group['qid'],lang));a=cur.fetchone()
            if a:out.setdefault('full_article_text',{})[lang]=a['wikitext']
    c.close();return out

def valid_flag(flag,payload):
    allowed={'src':['Contradicted','Not in source'],'lang':['Versions differ'],'tone':['Loaded wording'],'fact':['Numbers differ','Dates differ','Names differ']}
    if flag.get('verdict') not in allowed.get(flag.get('check'),[]):
        target={'Missing in Finnish':'fi','Missing in Swedish':'sv','Missing in English':'en','Missing in German':'de','Missing in Russian':'ru'}.get(flag.get('verdict'))
        if flag.get('check')!='lang' or not target or target not in payload.get('full_article_text',{}):return False
    rows={r['id']:r for cs in payload['candidates'].values() for r in cs};cid=flag.get('claim_id')
    if cid not in rows or rows[cid]['lang']!=flag.get('language'):return False
    if not flag.get('marks') or not flag['marks'].get(cid):return False
    for claim_id,marks in flag['marks'].items():
        if claim_id not in rows or any(not m or m not in rows[claim_id]['text'] for m in marks):return False
        if flag['check'] in ['lang','fact'] and rows[claim_id]['lang'] in ['de','ru']:return False
    sid=flag.get('source_id');passage=flag.get('source_passage')
    if flag['check']=='src':
        if sid not in {s['id'] for s in rows[cid]['citations']} or sid not in payload['sources']:return False
        s=payload['sources'][sid];text=s.get('full_source_text') or '\n'.join(p['text'] for p in s['passages'])
        if s['status']!='Read':return False
        if not passage or passage not in text:return False
        if any(m not in passage for m in flag.get('source_marks',[])):return False
        if flag['verdict']=='Not in source' and 'full_source_text' not in s and payload.get('second_pass'):return False
    if flag.get('suggestion',{}):
        sug=flag['suggestion']
        if sug.get('type')=='language' and sug.get('source_id') not in payload['sources']:return False
    return True

def store_judge(group_id,result):
    c=db();cur=c.cursor();cur.execute('REPLACE INTO judgment VALUES (%s,%s,%s,%s,%s,%s,%s)',(digest([group_id,result['model'],result['input_sha256']]),group_id,result['model'],result['prompt_version'],result['checked_at'].replace('T',' ').replace('Z',''),result['input_sha256'],json.dumps(result,ensure_ascii=False)));c.close()

def process_batch(groups):
    inputs=[evidence(g) for g in groups]
    articles=full_articles(groups[0]['qid'])
    first=judge(FAST,RECALL_PROMPT,{'groups':inputs},version=VERSION)
    for payload in inputs:payload['full_article_text']=articles
    byid={g['id']:g for g in groups};inputs_byid={g['id']:g for g in inputs}
    outputs=[]
    for answer in first['answer'].get('groups',[]):
        gid=answer.get('id')
        if gid not in byid:continue
        group=byid[gid];store_judge(gid,first)
        versions={};rows={r['id']:r for rs in inputs_byid[gid]['candidates'].values() for r in rs}
        for lang,v in answer.get('versions',{}).items():
            if v.get('claim_id') not in rows or rows[v['claim_id']]['lang']!=lang:continue
            versions[lang]={**rows[v['claim_id']],**v}
        candidates=[f for f in answer.get('flags',[]) if f.get('check') in ['src','fact','lang','tone'] and f.get('claim_id') in rows]
        agreed=[]
        if candidates:
            payload=evidence(group,full=True);payload['second_pass']=True
            payload['investigate_checks']=list(dict.fromkeys(f['check'] for f in candidates))
            # No first-pass summaries, verdicts or reasons are supplied to the reviewer.
            second=judge(STRONG,PRECISION_PROMPT,{'groups':[payload]},namespace='rechecks',version=VERSION,context={'full_article_text':articles});store_judge(gid,second)
            payload['full_article_text']=articles
            answers=second['answer'].get('groups',[])
            if answers:
                checked=answers[0]
                strong_versions={}
                all_rows={r['id']:r for rs in payload['candidates'].values() for r in rs}
                for lang,v in checked.get('versions',{}).items():
                    if v.get('claim_id') in all_rows and all_rows[v['claim_id']]['lang']==lang:strong_versions[lang]={**all_rows[v['claim_id']],**v}
                for f in checked.get('flags',[]):
                    if not valid_flag(f,payload):continue
                    if f['language'] in ['fi','sv','en']:
                        # Strong pass supplies final presentation text; all quotes remain fetched literals.
                        f['id']=digest([gid,f['claim_id'],f['check'],f['verdict']])[:32];f['group_id']=gid;f['qid']=group['qid'];f['models']=[FAST,STRONG];f['prompt_version']=VERSION;f['checked_at']=now();f['history']=None
                        f['current_confirmed']=True
                        f['versions']=strong_versions
                        if not set(f['marks']).issubset({v['claim_id'] for v in strong_versions.values()}):continue
                        attach_source(f,payload)
                        agreed.append(f)
        c=db();cur=c.cursor()
        if agreed:versions=agreed[0]['versions']
        cur.execute('REPLACE INTO claim_group VALUES (%s,%s,%s,%s,%s,%s)',(gid,group['qid'],group['anchor_id'],group['ordinal'],json.dumps(versions,ensure_ascii=False),json.dumps({'prompt_version':VERSION,'first_pass':first['checked_at'],'candidate_flags':len(candidates),'agreed_flags':len(agreed)})))
        for lang,v in versions.items():cur.execute('UPDATE claim SET gloss=%s WHERE id=%s',(v.get('gloss'),v['claim_id']))
        for f in agreed:
            cur.execute('INSERT INTO flag VALUES (%s,%s,%s,%s,%s,%s,%s,0,%s) ON DUPLICATE KEY UPDATE payload=VALUES(payload),checked_at=VALUES(checked_at)',(f['id'],f['qid'],gid,f['claim_id'],f['check'],f['verdict'],json.dumps(f,ensure_ascii=False),f['checked_at'].replace('T',' ').replace('Z','')))
        ids=[f['id'] for f in agreed]
        cur.execute('UPDATE flag SET shown=0,payload=JSON_SET(payload,\'$.current_confirmed\',false) WHERE group_id=%s'+(' AND id NOT IN ('+','.join(['%s']*len(ids))+')' if ids else ''),(gid,*ids))
        c.close();outputs+=agreed
    print('checked',len(groups),'groups; independently agreed',len(outputs),'flags',flush=True)
    return outputs

def main():
    p=argparse.ArgumentParser();p.add_argument('--qid',default='Q134949');p.add_argument('--workers',type=int,default=4);p.add_argument('--batch-size',type=int,default=12);p.add_argument('--limit',type=int);args=p.parse_args()
    groups=build_groups(args.qid);c=db();cur=c.cursor();cur.execute("SELECT id FROM claim_group WHERE qid=%s AND JSON_UNQUOTE(JSON_EXTRACT(checks,'$.prompt_version'))=%s",(args.qid,VERSION));done={r['id'] for r in cur.fetchall()}
    cur.execute("SELECT DISTINCT cs.claim_id FROM claim_source cs JOIN cited_source s ON s.id=cs.source_id JOIN claim cl ON cl.id=cs.claim_id WHERE cl.qid=%s AND s.status='Read'",(args.qid,));read={r['claim_id'] for r in cur.fetchall()};c.close();groups=[g for g in groups if g['id'] not in done]
    import re
    groups.sort(key=lambda g:(g['anchor_id'] not in read,not bool(re.search(r'\d',next(r['text'] for rs in g['candidates'].values() for r in rs if r['id']==g['anchor_id']))),g['ordinal']))
    if args.limit:groups=groups[:args.limit]
    print('groups remaining',len(groups),flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(process_batch,[groups[i:i+args.batch_size] for i in range(0,len(groups),args.batch_size)]))
    c=db();cur=c.cursor();cur.execute("SELECT COUNT(*) n FROM claim_group WHERE qid=%s AND JSON_UNQUOTE(JSON_EXTRACT(checks,'$.prompt_version'))=%s",(args.qid,VERSION));done=cur.fetchone()['n']
    if done>=len(build_groups(args.qid)):cur.execute("UPDATE topic SET state='checked' WHERE qid=%s",(args.qid,))
    c.close()

if __name__=='__main__':main()
