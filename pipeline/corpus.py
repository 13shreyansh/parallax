import json,re,concurrent.futures, argparse
import pyarrow.parquet as pq
from .common import ROOT,WORK,wiki,db,init_db,now

def manifest():
    path=WORK/'manifest.json'
    if path.exists():return json.loads(path.read_text())
    tables={l:pq.read_table(ROOT/f'work/vector-starter/data/articles-{l}.parquet',columns=['wikidata_id','page_id','rev_id','title','url','date_modified']).to_pylist() for l in ['fi','sv','en']}
    maps={l:{r['wikidata_id']:r for r in rows if r['wikidata_id']} for l,rows in tables.items()}
    shared=set.intersection(*(set(v) for v in maps.values()))
    # Theme membership comes from the sponsor category tree, not a handpicked top ten.
    children={}
    for line in (ROOT/'work/vector-starter/data/category-links-fi.tsv').read_text().splitlines()[1:]:
        p,c=line.split('\t');children.setdefault(p,[]).append(c)
    roots=[k for k in children if k in ['Suomi toisessa maailmansodassa','Talvisota','Jatkosota','Lapin sota']]
    war=set(roots);todo=list(roots)
    while todo:
        for c in children.get(todo.pop(),[]):
            if c not in war:war.add(c);todo.append(c)
    war_pages=set()
    for line in (ROOT/'work/vector-starter/data/article-categories-fi.tsv').read_text().splitlines()[1:]:
        pid,cat=line.split('\t')
        if cat in war:war_pages.add(int(pid))
    rows=[{'qid':q,'versions':{l:maps[l][q] for l in maps},'themes':['history-of-finland']+(['finland-second-world-war'] if maps['fi'][q]['page_id'] in war_pages else [])} for q in shared]
    rows.sort(key=lambda r:(r['qid']!='Q134949','finland-second-world-war' not in r['themes'],r['versions']['en']['title']))
    path.write_text(json.dumps(rows,ensure_ascii=False));return rows

def register():
    init_db();c=db();cur=c.cursor()
    cur.executemany('REPLACE INTO theme VALUES (%s,%s)',[('history-of-finland','History of Finland'),('finland-second-world-war','Finland in the Second World War')])
    for row in manifest():
        cur.execute('INSERT IGNORE INTO topic(qid,title,titles) VALUES (%s,%s,%s)',(row['qid'],row['versions']['en']['title'],json.dumps({l:v['title'] for l,v in row['versions'].items()},ensure_ascii=False)))
        cur.executemany('INSERT IGNORE INTO topic_theme VALUES (%s,%s)',[(row['qid'],s) for s in row['themes']])
    c.close()

def fetch_batch(lang,versions):
    directory=WORK/'articles';directory.mkdir(exist_ok=True)
    missing=[v for v in versions if not (directory/f'{lang}-{v["page_id"]}.json').exists()]
    byid={v['page_id']:v for v in missing}
    for start in range(0,len(missing),20):
        batch=missing[start:start+20]
        j=wiki(lang,{'action':'query','pageids':'|'.join(str(v['page_id']) for v in batch),'prop':'revisions','rvprop':'ids|timestamp|content','rvslots':'main'})
        for page in j['query']['pages']:
            if page.get('missing') or not page.get('revisions'):continue
            v=byid[page['pageid']];rev=page['revisions'][0]
            a={'qid':v['wikidata_id'],'lang':lang,'page_id':page['pageid'],'title':page['title'],'rev_id':rev['revid'],'revised_at':rev['timestamp'],'wikitext':rev['slots']['main']['content'],'origin':'Wikipedia API current revision','fetched_at':now()}
            (directory/f'{lang}-{page["pageid"]}.json').write_text(json.dumps(a,ensure_ascii=False))
        print('fetched',lang,min(start+20,len(missing)),'/',len(missing),flush=True)

def fetch_winter_extra():
    for lang,title in [('de','Winterkrieg'),('ru','Советско-финляндская война (1939—1940)')]:
        directory=WORK/'articles';directory.mkdir(exist_ok=True)
        if list(directory.glob(f'{lang}-*.json')):continue
        j=wiki(lang,{'action':'query','titles':title,'prop':'revisions','rvprop':'ids|timestamp|content','rvslots':'main'})
        p=j['query']['pages'][0];r=p['revisions'][0]
        a={'qid':'Q134949','lang':lang,'page_id':p['pageid'],'title':p['title'],'rev_id':r['revid'],'revised_at':r['timestamp'],'wikitext':r['slots']['main']['content'],'origin':'Wikipedia API current revision','fetched_at':now()}
        (directory/f'{lang}-{p["pageid"]}.json').write_text(json.dumps(a,ensure_ascii=False))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--winter-only',action='store_true');args=parser.parse_args()
    register();rows=manifest()
    if args.winter_only:rows=rows[:1]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(lambda l:fetch_batch(l,[r['versions'][l] for r in rows]),['fi','sv','en']))
    fetch_winter_extra()

if __name__=='__main__':main()
