"""Synthetic controlled edits to real article sentences. Not human labels or source truth."""
import sys,pathlib,json,re,time,statistics
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from server.checks import check,baseline,dates
from server.db import connect,ALIGN_SQL,ASOF_SQL
import numpy as np
passages=json.load(open(ROOT/'data/passages.json'));split=json.load(open(ROOT/'eval/split.json'))
from scripts.ingest import chunks
confirmation=json.load(open(ROOT/'work/confirmation-articles.json'))
split['confirmation']=[a['wikidata_id'] for a in confirmation]
for a in confirmation:
 for i,(sec,text) in enumerate(chunks(a['text'])):passages.append({'id':f"confirmation-{a['page_id']}-{i}",'qid':a['wikidata_id'],'lang':'en','text':text})
# Pick sentences with full dates before scoring, deterministic order by passage ID.
cases=[]
for q in split['dev']+split['heldout']+split['confirmation']:
 ps=[p for p in passages if p['qid']==q and p['lang']=='en' and dates(p['text'])]
 for p in ps[:4]:
  original=p['text'];date=sorted(dates(original))[0];year,month,day=map(int,date.split('-'))
  daymatch=re.search(r'\b'+str(day)+r'\s+[A-Za-z]+\s+'+str(year)+r'\b',original)
  if not daymatch:continue
  s='dev' if q in split['dev'] else 'confirmation' if q in split['confirmation'] else 'heldout'
  # Expected outcomes are produced by mutation construction, never inferred labels.
  variants=[('unchanged',original,False),('extra-context',original+' A separate event occurred in 1922.',False)]
  newday=day+1 if day<27 else day-1
  variants += [('changed-day',original[:daymatch.start()]+str(newday)+original[daymatch.start()+len(str(day)):],True),('changed-year',original.replace(str(year),str(year+1),1),True)]
  if 'Finland' in original:variants.append(('changed-name',original.replace('Finland','Sweden',1),True))
  for kind,target,flag in variants:cases.append({'id':p['id']+'-'+kind,'qid':q,'split':s,'kind':kind,'a':original,'b':target,'expected_review':flag,'similarity':1.0,'label_origin':'synthetic controlled edit'})
# Different event dates should not be automatically called contradictory.
for q in split['dev']+split['heldout']+split['confirmation']:
 p=next((p for p in passages if p['qid']==q and p['lang']=='en' and dates(p['text'])),None)
 if p:
  cases.append({'id':p['id']+'-different-event','qid':q,'split':'dev' if q in split['dev'] else 'confirmation' if q in split['confirmation'] else 'heldout','kind':'different-event','a':p['text'],'b':'A later commemoration took place on 1 January 2001.','expected_review':False,'similarity':.4,'label_origin':'synthetic negative control'})
rows=[];traces=[]
for s in ['dev','heldout','confirmation']:
 for method in ['Naive numeral mismatch','Guarded date/unit rules']:
  subset=[c for c in cases if c['split']==s];tp=fp=tn=fn=0;times=[]
  for c in subset:
   t=time.perf_counter();out=baseline(c['a'],c['b']) if method.startswith('Naive') else check(c['a'],c['b'],c['similarity']);times.append((time.perf_counter()-t)*1000)
   pred=out if isinstance(out,bool) else out['kind'] in ['date-review','numeric-review']
   tp+=int(pred and c['expected_review']);fp+=int(pred and not c['expected_review']);tn+=int(not pred and not c['expected_review']);fn+=int(not pred and c['expected_review'])
   traces.append({**c,'method':method,'prediction':pred,'output':out,'pass':pred==c['expected_review']})
  rows.append({'split':('initial held-out, already seen' if s=='heldout' else 'fresh held-out' if s=='confirmation' else s),'method':method,'n':len(subset),'positive':tp+fn,'negative':fp+tn,'tp':tp,'fp':fp,'tn':tn,'fn':fn,'recall':f'{tp}/{tp+fn} ({100*tp/(tp+fn):.1f}%)' if tp+fn else 'N/A','fpr':f'{fp}/{fp+tn} ({100*fp/(fp+tn):.1f}%)' if fp+tn else 'N/A','p50_ms':statistics.median(times)})
json.dump(cases,open(ROOT/'eval/cases.json','w'),ensure_ascii=False,indent=2)
json.dump(traces,open(ROOT/'eval/traces.json','w'),ensure_ascii=False,indent=2)
result={'summary':'Controlled edits to real English sentences from disjoint development and held-out articles. Labels are synthetic construction labels. Similarity is fixed at 1 for edited copies; these tests isolate the rules and do not test the retrieval pipeline.','rows':rows,'limitations':'No human labels, calibrated model judges, whole-article LLM baseline, or real-world contradiction accuracy. The initial held-out scores were seen before v2; only the fresh held-out articles were reserved before that change. Name swaps remain outside the rules and are counted as misses. Model/API cost for these local rules is zero; hardware and hosting costs are not estimated.'}
json.dump(result,open(ROOT/'public/evaluation.json','w'),indent=2)
print(json.dumps(rows,indent=2))
