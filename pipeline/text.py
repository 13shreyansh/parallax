"""Rendered-word matching without fetching or model inference."""
import re,html
def normalize(text):
    text=re.sub(r'<!--.*?-->',' ',text,flags=re.S)
    text=re.sub(r'<ref\b[^>]*?/\s*>|<ref\b[^>]*>.*?</ref\s*>',' ',text,flags=re.I|re.S)
    def template(m):
        p=m.group()[2:-2].split('|');name=p[0].strip().lower()
        if name in ('convert','cvt','val','num'):return ' '.join(p[1:3])
        if name in ('nowrap','nobr','small','lang','lang-fi','lang-sv','lang-en'):return p[-1]
        if name in ('snd','spaced ndash','ndash'):return '–'
        return ' '
    for _ in range(15):
        updated=re.sub(r'\{\{[^{}]*\}\}',template,text)
        if updated==text:break
        text=updated
    text=re.sub(r'\[\[(?:[^\]|]+\|)?([^\]]+)\]\]',r'\1',text)
    text=re.sub(r"'{2,}",'',text);text=re.sub(r'<[^>]+>',' ',text)
    return re.sub(r'\s+',' ',html.unescape(text)).strip()
