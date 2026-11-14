"""Rendered-word matching without fetching or model inference."""
import re,html,difflib
from collections import Counter,defaultdict
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

STOP=set('the and that with from this were was had for its into their they which also than them are has have not of in on to a an as by is at it be or but ja oli ovat sekä myös että kun sen hän de och som att med från till den det var en ett av på för hade inte'.split())
def words(text):
    return {w for w in re.findall(r'[^\W_]+',text.casefold()) if len(w)>2 and w not in STOP}

class HistoricalIndex:
    def __init__(self,text):
        self.text=normalize(text)
        self.sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+',self.text) if len(s.strip())>20]
        self.tokens=[words(s) for s in self.sentences];self.index=defaultdict(set)
        for i,tokens in enumerate(self.tokens):
            for token in tokens:self.index[token].add(i)
    def match(self,claim):
        needle=normalize(claim)
        if needle in self.text:return needle
        tokens=words(needle);votes=Counter(i for token in tokens for i in self.index.get(token,()))
        best=None;best_score=0
        for i,shared in votes.most_common(5):
            other=self.tokens[i]
            if shared<min(3,len(tokens)) or shared/max(1,len(tokens|other))<.35:continue
            score=difflib.SequenceMatcher(None,needle.casefold(),self.sentences[i].casefold(),autojunk=False).ratio()
            if score>=.62 and score>best_score:best=self.sentences[i];best_score=score
        return best

def historical_passage(claim,text):
    return HistoricalIndex(text).match(claim)
