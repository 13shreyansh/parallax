"""Resolve named refs before sentence splitting; preserve exact rendered wording."""
import re, html
import mwparserfromhell as mw
from .common import digest

STOP=re.compile(r'^(references|notes|sources|bibliography|external links|see also|lähteet|viitteet|kirjallisuus|källor|referenser|noter|litteratur|webblänkar|einzelnachweise|literatur|примечания|литература|ссылки)$',re.I)

def plain(s):
    code=mw.parse(s)
    for t in reversed(code.filter_templates()):
        name=str(t.name).strip().lower()
        if name in ('nowrap','nobr','small','lang','lang-fi','lang-sv','lang-en'):
            vals=[str(p.value) for p in t.params];code.replace(t,vals[-1] if vals else '')
        elif name in ('convert','cvt','val','num'):
            code.replace(t,' '.join(str(p.value).strip() for p in list(t.params)[:2]))
        elif name in ('snd','spaced ndash','ndash'):code.replace(t,'–')
        else:code.replace(t,'')
    return re.sub(r'\s+',' ',html.unescape(code.strip_code(normalize=True,collapse=True))).strip()

def citations(wikitext):
    named={};refs=[]
    for tag in mw.parse(wikitext).filter_tags():
        if str(tag.tag).lower()!='ref':continue
        name=next((str(a.value).strip('"\' ') for a in tag.attributes if str(a.name).strip()=='name'),None)
        content=str(tag.contents or '')
        if content.strip() and name:named[name]=content
        refs.append((str(tag),name,content))
    return named,refs

def ref_record(content):
    code=mw.parse(content)
    urls=[];meta={}
    for link in code.filter_external_links():urls.append(str(link.url).strip())
    for t in code.filter_templates():
        for p in t.params:
            key=str(p.name).strip().lower();v=str(p.value).strip()
            if key in ['url','archive-url','archiveurl','verkko-osoite','osoite']:urls.append(v)
            if key in ['title','otsikko','nimeke','titel','teos','isbn','page','pages','sivu','sivut','date','year']:meta[key]=plain(v)
    urls+=re.findall(r'https?://[^\s<>\[\]{}|]+',content)
    urls=list(dict.fromkeys(u.rstrip('.,;') for u in urls if u.startswith(('http://','https://'))))
    return {'id':digest(content)[:32],'content':content,'label':plain(content),'urls':urls,'metadata':meta,'status':'pending' if urls else 'Book, not checked'}

def split_claims(article):
    text=re.sub(r'<!--.*?-->','',article['wikitext'],flags=re.S)
    named,refs=citations(text);refmap={}
    def replace_ref(match):
        raw=match.group();tag=mw.parse(raw).filter_tags()[0]
        name=next((str(a.value).strip('"\' ') for a in tag.attributes if str(a.name).strip()=='name'),None)
        content=str(tag.contents or '').strip() or named.get(name,'')
        if not content:return ''
        rec=ref_record(content);refmap[rec['id']]=rec
        return f' REF{rec["id"]} '
    text=re.sub(r'<ref\b[^>]*?/\s*>|<ref\b[^>]*>.*?</ref\s*>',replace_ref,text,flags=re.I|re.S)
    # Short footnotes are real citations too. Resolve only unambiguous bibliography entries.
    bibliographies=[]
    for t in mw.parse(text).filter_templates():
        if str(t.name).strip().lower().startswith(('cite ','citation','kirjaviite','verkkoviite')):
            fields={str(p.name).strip().lower():str(p.value).strip() for p in t.params}
            names=[v.casefold() for k,v in fields.items() if k.startswith(('last','author','tekijä','sukunimi'))]
            years=re.findall(r'\b(?:18|19|20)\d{2}[a-z]?\b',' '.join(v for k,v in fields.items() if k in ['year','date','vuosi','ajankohta']))
            bibliographies.append((names,years,str(t)))
    code=mw.parse(text)
    for t in reversed(code.filter_templates()):
        if str(t.name).strip().lower() not in ['sfn','sfnp','sfnm','harvnb','harv','harvtxt']:continue
        vals=[str(p.value).strip() for p in t.params if str(p.name).strip().isdigit()]
        names=[v.casefold() for v in vals if not re.match(r'^\d',v)]
        years=[v for v in vals if re.match(r'^(?:18|19|20)\d{2}',v)]
        matches=[raw for ns,ys,raw in bibliographies if names and years and any(n in ns for n in names) and any(y in ys for y in years)]
        content=matches[0] if len(matches)==1 else str(t)
        rec=ref_record(content);rec['label']=rec['label'] or ', '.join(vals);refmap[rec['id']]=rec
        code.replace(t,f' REF{rec["id"]} ')
    text=str(code)
    text=re.sub(r'\{\|.*?\|\}','',text,flags=re.S)
    text=re.sub(r'<(?:gallery|timeline|math|score)\b.*?</(?:gallery|timeline|math|score)>','',text,flags=re.S|re.I)
    section='Introduction';rows=[]
    for line in text.splitlines():
        if re.match(r'^={2,}',line):
            section=plain(line.strip('= '));continue
        if STOP.match(section) or not line.strip() or line.lstrip().startswith(('|','!','{{','}}','[[File:','[[Tiedosto:','[[Fil:','[[Category:','[[Luokka:','[[Kategori:')):continue
        cleaned=plain(line.lstrip('*#:; '))
        if len(cleaned)<35:continue
        # Keep trailing reference markers on the sentence they follow, including refs after punctuation.
        sentences=re.sub(r'([.!?])((?:\s+REF[0-9a-f]{32})*)\s+(?!REF[0-9a-f]{32})(?=[A-ZÄÖÅА-ЯÉ0-9])',r'\1\2␞',cleaned).split('␞')
        sentence_refs=[re.findall(r'REF([0-9a-f]{32})',s) for s in sentences]
        paragraph_quote=re.sub(r'\s*REF[0-9a-f]{32}\s*',' ',cleaned).strip()
        for sentence_index,s in enumerate(sentences):
            ids=sentence_refs[sentence_index]
            inherited=False
            if not ids:
                # A paragraph-ending reference can support its preceding sentences.
                # Preserve that scope explicitly for the precision gate to inspect.
                ids=next((refs for refs in sentence_refs[sentence_index+1:] if refs),[])
                inherited=bool(ids)
            quote=re.sub(r'\s*REF[0-9a-f]{32}\s*',' ',s).strip()
            quote=re.sub(r'\s+',' ',quote)
            if len(quote)<35:continue
            # Extremely long bulleted/list prose remains one verifiable unit, never silently capped.
            refs=[{**refmap[i],'citation_scope':'paragraph-ending' if inherited else 'sentence','paragraph_text':paragraph_quote} for i in ids]
            rows.append({'id':digest([article['qid'],article['lang'],article['rev_id'],len(rows),quote])[:32],'qid':article['qid'],'lang':article['lang'],'rev_id':article['rev_id'],'ordinal':len(rows),'section':section,'text':quote,'citations':refs})
    return rows
