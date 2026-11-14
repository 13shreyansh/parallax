"""Fetch and cache all citation URLs. Failed/offline sources are never flagged."""
import json,re,ipaddress,socket,urllib.parse,concurrent.futures
import requests,trafilatura,fitz
from .common import WORK,UA,digest,now

def book_preview(url):
    p=urllib.parse.urlsplit(url)
    return p.netloc in ['books.google.com','books.google.fi','books.google.se','books.google.de','www.worldcat.org','openlibrary.org'] or (p.netloc=='archive.org' and p.path.startswith('/details/'))

def public_url(url):
    try:
        p=urllib.parse.urlsplit(url)
        if p.scheme not in ['http','https'] or p.username or p.password or p.port not in [None,80,443]:return False
        return all(ipaddress.ip_address(x[4][0]).is_global for x in socket.getaddrinfo(p.hostname,p.port or 443))
    except (ValueError,OSError):return False

def read_url(url):
    if not public_url(url):return None
    try:
        # Validate each redirect too: public citations may not reach internal services.
        for _ in range(6):
            r=requests.get(url,headers={'User-Agent':UA},timeout=(8,18),stream=True,allow_redirects=False)
            if r.is_redirect:
                url=urllib.parse.urljoin(url,r.headers['location']);r.close()
                if not public_url(url):return None
                continue
            if r.status_code!=200:r.close();return None
            data=bytearray()
            for chunk in r.iter_content(65536):
                data.extend(chunk)
                if len(data)>15_000_000:r.close();return None
            typ=r.headers.get('content-type','');r.close()
            if 'pdf' in typ or data[:4]==b'%PDF':
                doc=fitz.open(stream=bytes(data),filetype='pdf');text='\n'.join(p.get_text() for p in doc);title=(doc.metadata or {}).get('title') or urllib.parse.urlsplit(url).netloc
            else:
                # Let the HTML meta charset override requests' ISO-8859-1 default.
                raw=bytes(data)
                text=trafilatura.extract(raw,include_comments=False,include_tables=True,include_links=False,favor_recall=True)
                md=trafilatura.extract_metadata(raw);title=md.title if md and md.title else urllib.parse.urlsplit(url).netloc
            if text and len(text)>250 and not re.search(r'^(access denied|just a moment|enable javascript|verify you are human)',text.strip(),re.I):return {'text':text,'title':title,'final_url':url}
            return None
    except Exception:return None

def fetch_source(url):
    directory=WORK/'sources';directory.mkdir(exist_ok=True)
    sid=digest(url)[:32];p=directory/f'{sid}.json'
    if p.exists():
        cached=json.loads(p.read_text())
        if not re.search('[ÃÂ]',cached.get('text','')):
            if book_preview(url):cached['status']='Book, not checked'
            return cached
    result={'id':sid,'url':url,'status':'Source unreachable','text':'','title':urllib.parse.urlsplit(url).netloc,'read_at':now(),'archive_url':None}
    got=read_url(url)
    if not got:
        try:
            r=requests.get('https://archive.org/wayback/available',params={'url':url},headers={'User-Agent':UA},timeout=(6,12))
            snap=r.json().get('archived_snapshots',{}).get('closest',{})
            if snap.get('available'):
                archive=snap['url'].replace('http://','https://',1)
                got=read_url(archive)
                if got:result['archive_url']=archive
        except Exception:pass
    if got:
        result.update(got);result['status']='Read';result['content_sha256']=digest(got['text'])
        # A catalogue/preview page is not the cited book's contents.
        if book_preview(url):
            result['status']='Book, not checked'
    p.write_text(json.dumps(result,ensure_ascii=False));return result

def chunks(text,size=650):
    # Short overlapping windows fit the existing multilingual encoder's context.
    out=[];sentences=re.split(r'(?<=[.!?])\s+|\n+',text);buf=''
    for sent in sentences:
        if len(buf)+len(sent)>size and buf:
            out.append(buf);buf=buf[-120:]+' '+sent
        else:buf+=' '+sent
        while len(buf)>size*2:
            out.append(buf[:size]);buf=buf[size-100:]
    if buf.strip():out.append(buf.strip())
    return out
