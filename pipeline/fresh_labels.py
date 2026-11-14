import json,collections
from .common import ROOT,WORK,now
from .extract import split_claims
COUNTERPARTS={
'8ffe0f536440921b78f295e2d661f60a':('fi',5901,24312843,'78b59065c77b5dfb555bc8aca7cabe20'),
'84513e492515b70b2c155facd1e939ac':('fi',5901,24312843,'e222b06138b5b8fbb58742ab911ed4ca'),
'302a91dbf338f53eb5f4f4ce6bd8b9d1':('fi',5901,24312843,'175c834b16a0723193d5cbe55f416fc2'),
'cb271178e17fd02640dd447af27fe6ad':('fi',156802,24352919,'422a6717fa6f90bd713f0c77959ff31a'),
'14addaf85490418ae9e97073c36b342e':('sv',7855244,59261236,'f54593bf0ce85a7f7047266d602771a2'),
'62d01c602046bcc66c9d393a73abe6aa':('fi',17105,24355094,'3892c689ae3b52f53986bbfd8d842289'),
'4d87dd18871488c70137cdb9f74185d6':('fi',17105,24355094,'b5139fbdf8a91011f1b13bd064a1299a'),
'3d84865ab0f003ea87434b64bf723539':('fi',17105,24355094,'5676a5dc3c75994fbb5acd1b35129504')}
def main():
 controls=[]
 for cid,kind,text,quote in json.loads((WORK/'fresh-controls-input.json').read_text()):
  original=json.loads((WORK/f'eval-fresh/{cid}.json').read_text());assert text in original['claim']['text'];assert quote in original['source']['text']
  row={'id':cid,'original_id':cid,'kind':kind,'clean_text':text,'source_quote':quote,'article_context':original['article']['title'],'construction':'intact claim' if text==original['claim']['text'] else 'exact supported excerpt'}
  if cid in COUNTERPARTS:
   lang,page,rid,claimid=COUNTERPARTS[cid];a=json.loads((WORK/f'articles/{lang}-{page}.json').read_text());assert a['rev_id']==rid
   cl=next(x for x in split_claims(a) if x['id']==claimid);row['counterpart']={'lang':lang,'page_id':page,'rev_id':rid,'claim_id':claimid,'text':cl['text']}
  controls.append(row)
 assert collections.Counter(x['kind'] for x in controls)==dict.fromkeys(['wrong_date','wrong_number','dropped_sentence','loaded_wording','unsupported_claim'],8)
 old=json.loads((ROOT/'eval/parallax/FROZEN.json').read_text());oldqids={x['article']['qid'] for x in old['case_metadata']};newqids={json.loads((WORK/f'eval-fresh/{x["id"]}.json').read_text())['article']['qid'] for x in controls};assert not oldqids&newqids
 result={'labeler':'gpt-6-astra','labeled_at':now(),'detector_output_seen':False,'controls':controls,'article_families':sorted(newqids),'scope':'40 source-supported controlled real-passage copies: 12 intact claims and 28 exact supported excerpts; eight real fi/sv counterparts. Labels were checked independently before the detector ran. This is not full-article population accuracy.'}
 (ROOT/'eval/parallax/FRESH-CONTROLS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('Fresh independent controls frozen',len(controls),collections.Counter(x['construction'] for x in controls))
if __name__=='__main__':main()
