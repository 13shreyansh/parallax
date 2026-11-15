"""Winter War development only. Never reads any held-out labels or outputs."""
import json
from .common import db,digest,WORK,ROOT,now
from .prompts_v5 import VERSION,PRECISION_PROMPT
from .check import process_batch
from .evaluate_v4 import setup

def main():
 c=db();cur=c.cursor();cur.execute("SELECT versions FROM claim_group WHERE qid='Q134949' ORDER BY id");fs=[{'versions':json.loads(r['versions'])} for r in cur.fetchall()];cases=[]
 for i,f in enumerate(fs):
  vs=f['versions'];en=vs.get('en');lang=next((l for l in ['fi','sv'] if l in vs),None)
  if not en or not lang:continue
  v=vs[lang];cur.execute("SELECT * FROM article WHERE qid='Q134949' AND lang='en'");a=cur.fetchone()
  cur.execute("SELECT s.* FROM cited_source s JOIN claim_source cs ON cs.source_id=s.id WHERE cs.claim_id=%s AND s.status='Read' LIMIT 1",(en['claim_id'],));source=cur.fetchone()
  if not source:continue
  for planted in [False,True]:
   ident=digest(['winter-coverage-dev',i,planted])[:32]
   cases.append({'id':ident,'qid':'D'+ident[:22],'text':'' if planted else en['text'],'planted':planted,'kind':'dropped_sentence','counterpart':{'lang':lang,'text':v['text']} if planted else None,'article':a,'source':source})
  if len(cases)>=6:break
 c.close();assert cases,'No development cases';groups=setup(cases,database='parallax_dev_coverage',include_title=True);results=[]
 for case in cases:
  flags=[f for g in groups[case['id']] for f in process_batch([g],precision_prompt=PRECISION_PROMPT,version=VERSION)]
  results.append({'id':case['id'],'planted':case['planted'],'caught':any(f['verdict']=='Missing in English' for f in flags),'flags':len(flags)})
 out={'at':now(),'scope':'Winter War controlled-copy development only; not accuracy measurement','prompt_sha256':digest(PRECISION_PROMPT),'results':results};(WORK/'coverage-dev-v5.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
if __name__=='__main__':main()
