"""Conservative review rules. A review lead is never a factual verdict."""
import re,unicodedata
MONTHS={
 'january':1,'tammikuuta':1,'januari':1,'february':2,'helmikuuta':2,'februari':2,
 'march':3,'maaliskuuta':3,'mars':3,'april':4,'huhtikuuta':4,
 'may':5,'toukokuuta':5,'maj':5,'june':6,'kesäkuuta':6,'juni':6,
 'july':7,'heinäkuuta':7,'juli':7,'august':8,'elokuuta':8,'augusti':8,
 'september':9,'syyskuuta':9,'september':9,'october':10,'lokakuuta':10,'oktober':10,
 'november':11,'marraskuuta':11,'december':12,'joulukuuta':12,'december':12}
def dates(text):
 s=unicodedata.normalize('NFKC',text).lower();out=set()
 for d,m,y in re.findall(r'\b(\d{1,2})\.?\s+('+ '|'.join(MONTHS)+r')\s+(\d{4})\b',s):out.add(f'{int(y):04}-{MONTHS[m]:02}-{int(d):02}')
 return out
def numbers(text):
 s=unicodedata.normalize('NFKC',text)
 s=re.sub(r'(?<=\d)[\u00a0\u202f ](?=\d{3}\b)','',s)
 return set(re.findall(r'(?<!\w)\d+(?:[.,]\d+)?%?',s))
def baseline(a,b):return numbers(a)!=numbers(b)
def check(a,b,similarity=1):
 da,db=dates(a),dates(b)
 # Matching dates are strong agreement for those dates, not for the whole passage.
 if da and db and da==db:
  return {'kind':'aligned','reason':'The extracted full dates match. Other claims still need source review.','dates_a':sorted(da),'dates_b':sorted(db)}
 if similarity>=.86 and da and db and len(da)==len(db) and da!=db:
  return {'kind':'date-review','reason':'Very similar passages contain a changed full date. Check whether they describe the same event, calendar and scope.','dates_a':sorted(da),'dates_b':sorted(db)}
 # Restrict count warnings to matching units to avoid flagging any two numerals.
 pattern=r'(\d+(?:[.,]\d+)?)\s*(%|percent|procent|prosenttia|km|kilometriä|kilometers|days|päivää|dagar)\b'
 ua={u.replace('prosenttia','%').replace('procent','%').replace('percent','%'):n.replace(',','.') for n,u in re.findall(pattern,a.lower())}
 ub={u.replace('prosenttia','%').replace('procent','%').replace('percent','%'):n.replace(',','.') for n,u in re.findall(pattern,b.lower())}
 conflicts=[{'unit':u,'a':ua[u],'b':ub[u]} for u in ua.keys()&ub.keys() if ua[u]!=ub[u]]
 if similarity>=.86 and conflicts:return {'kind':'numeric-review','reason':'A matching unit has different values. Rounding, scope or context may explain the difference.','values':conflicts}
 if similarity<.48:return {'kind':'coverage','reason':'No close passage was retrieved in the other language. This may be a coverage difference or a retrieval miss.'}
 return {'kind':'emphasis','reason':'Related passages were found. Different wording or emphasis is not evidence of a factual contradiction.'}
def tone(text):
 terms=['heroic','glorious','cowardly','barbaric','sankarillinen','urhoollinen','héroïque']
 return [t for t in terms if re.search(r'\b'+re.escape(t)+r'\b',text.lower())]
def source_state(text):
 if re.search(r'citation needed|källa\s*behövs|lähde\??',text,re.I):return {'status':'cannot-verify','reason':'The stored passage contains a citation-needed marker. No cited-source excerpt has been verified.'}
 return {'status':'cannot-verify','reason':'This text snapshot does not provide a verified source excerpt for this passage. Agreement between Wikipedias is not source verification.'}
