"""Record the two blind partitions and publish only independently confirmed evidence."""
import json
from .common import db,WORK,ROOT,now
UNCONFIRMED={
4:(False,'460 versus approximately 500 is compatible rounding; airfield and municipality scopes differ.'),
5:(False,'German transit arrangements are already covered; the missing request date and route are extra detail.'),
7:(None,'Different predecessors may refer to overall forces, a new front, or one army; identical command scope is not established.'),
13:(False,'The discovered generator and its condition are incidental equipment details.'),
14:(False,'Finnish already covers recipient age; the older subgroup count and oldest person add optional detail.'),
20:(None,'A short programme catalogue cannot establish absence of a first-documentary assertion or exclude individual production roles.'),
25:(False,'Finnish already identifies the first non-officer recipient and award date; the combat anecdote is optional detail.'),
34:(False,'English covers prewar mobilisation; this separate covering-force movement date does not establish a substantial missing event.'),
35:(False,'One defensive gap location and width are optional tactical detail in the concise Swedish overview.'),
41:(False,'Finnish covers border fighting and anti-tank methods; the 80-tank subtotal is additional detail.'),
46:(False,'Truck sales and later inventory counts are incidental postwar equipment-disposal details.'),
47:(False,'English lists the book; the missing sentence adds archival provenance without substantive findings.'),
48:(False,'Finnish covers food shortages and German imports; one request date and tonnage are additional detail.'),
50:(False,'English covers the diary; manuscript page count and repositories are incidental archival details.'),
53:(None,'Parliamentary war-status recognition and the presidential broadcast are distinct events, so identical date scope is unproven.'),
60:(False,'A generic rhetorical line inside an attributed Khrushchev quote is not substantive missing factual coverage.')}
REASONS={2:'Swedish omits official versus archival Soviet tank-loss estimates.',1:'Specific Soviet peace overture of8February1943 is absent from the complete English account.',3:'The60percent Petsamo nickel allocation to Germany is substantive economic cooperation absent from English.',6:'Swedish omits the recipients young age profile.',8:'Postwar Soviet reform review is distinct from wartime retraining and absent from Swedish.',9:'Swedish omits geographical distribution of Mannerheim Cross recipients.',10:'Finnish omits defensive strongpoint scale and early construction history.',11:'Swedish omits the invading7thArmies composition and deployment.',12:'Swedish omits Korhonens1948 account in the theorys substantive development.',15:'English omits signals intelligence as a distinct operational capability.',16:'Five navy awards versus seven navy recipients is a same-population discrepancy requiring review.',17:'Swedish omits the evacuation of approximately100000Lapland civilians.',18:'Finnish omits the Raate Road casualty comparison.',19:'English second-award prose says26June; peer versions and its own list say28June1944.',21:'English omits Finnish submarines mining the Estonian coast.',22:'Same parliamentary decision has108to43 versus113to43 votes.',23:'Swedish omits the25October1942 peace initiative and Rytis nonresponse.',24:'English omits the Ayräpää–Vuosalmi March operation and force imbalance.',26:'Same award/person is dated8February versus8March1943.',27:'Swedish omits the substantive log-boat revision of the driftwood theory.',28:'Swedish omits Finnish attrition and exhaustion before the main offensive.',29:'Same official casualty report gives48475 versus48745, anchored by identical158863 accompanying figure.',30:'English omits geographical recipient distribution.',31:'Finnish omits overall fighter victories and aircraft losses.',32:'Swedish omits deportation incident and subsequent refusal to transfer more Jews.',33:'English omits Finnish command orders for Estonian coast minelaying.',36:'Swedish omits the1967 proposal to resume awards.',37:'Reciprocal navy-award population discrepancy.',38:'Reciprocal same-report casualty digit discrepancy.',39:'Swedish omits the60percent nickel allocation.',40:'Finnish omits the asserted Soviet influence on Rytis election.',42:'The study is dated1987 versus1988 in the articles and bibliographies.',43:'Finnish omits competing Soviet tank-loss estimates.',44:'Finnish qualification of aircraft tank-destruction claims is absent from English effectiveness account.',45:'English omits Paasikivis Stockholm channel and delivery of peace conditions.',49:'Swedish omits lifting the Leningrad siege before the1944offensive.',51:'Swedish omits British Operation Benedict training/support.',52:'Finnish omits broader national-unity response to invasion.',54:'Swedish omits the167976named-record estimate and archival basis.',55:'British ultimatum deadlines differ3December versus5December.',56:'English omits Finnish installation of bomber radio-navigation equipment.',57:'English omits the Soviet demand for a signed surrender/peace request before a delegation.',58:'Swedish omits overall Finnish fighter victories and losses.',59:'The complete film review describes a sniper chained to a rock, not the asserted historical tree-branch nest practice.'}
DDL='CREATE TABLE IF NOT EXISTS independent_review (flag_id CHAR(32) PRIMARY KEY,confirmed BOOLEAN,reason TEXT NOT NULL,reviewer VARCHAR(100) NOT NULL,reviewed_at DATETIME NOT NULL,round_name VARCHAR(40) NOT NULL)'
def main():
 assert set(UNCONFIRMED)|set(REASONS)==set(range(1,61))
 assert len(REASONS)==44 and len(UNCONFIRMED)==16
 c=db();cur=c.cursor();cur.execute(DDL)
 early=json.loads((ROOT/'eval/parallax/BLIND-REAL.json').read_text())
 for r in early['assessments']:
  cur.execute('REPLACE INTO independent_review VALUES (%s,%s,%s,%s,UTC_TIMESTAMP(),%s)',(r['flag_id'],r['confirmed'],r['reason'],'gpt-6-astra','winter-war-early'))
 manifest=json.loads((WORK/'blind-final/manifest-private.json').read_text());rows=[]
 for i in range(1,61):
  fid=manifest['mapping'][str(i)];confirmed,reason=UNCONFIRMED.get(i,(True,REASONS.get(i,'')));assert reason
  case=json.loads((WORK/f'blind-final/case-{i:02}.json').read_text())
  cur.execute('REPLACE INTO independent_review VALUES (%s,%s,%s,%s,UTC_TIMESTAMP(),%s)',(fid,confirmed,reason,'gpt-6-astra','theme-random-60'))
  if confirmed is not True:
   cur.execute('SELECT claim_id,check_type,verdict FROM flag WHERE id=%s',(fid,));f=cur.fetchone();cur.execute('REPLACE INTO quality_exclusion VALUES (%s,%s,%s,%s,%s,%s,UTC_TIMESTAMP())',(fid,f['claim_id'],f['check_type'],f['verdict'],reason,'gpt-6-astra'))
  rows.append({'case':i,'flag_id':fid,'confirmed':confirmed,'reason':reason,'check':case['check_type'],'claim':case['claim'],'article_files':case['full_article_files'],'sources':case['cited_sources']})
 result={'reviewer':'gpt-6-astra','review_design':'Two read-only partitions of30 from one seeded random sample; grouped by topic only after sampling to avoid redundant whole-article reads. No detector verdicts, summaries, reasons, private mapping or previous reviews were shown.','measured_at':now(),'sampled_at':manifest['sampled_at'],'seed':manifest['seed'],'population':manifest['population'],'sample_size':60,'confirmed':44,'false':13,'uncertain':3,'precision':44/60,'scope':'Random sample of 60 from 317 published theme flags before additional independent-review curation. Uncertain counts as unconfirmed. This 73.3 percent measures the pre-curation population; it is not a precision estimate of the subsequently filtered list.','assessments':rows}
 (ROOT/'eval/parallax/BLIND-FINAL.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 cur.execute('REPLACE INTO evaluation VALUES (%s,%s,UTC_TIMESTAMP())',('blind_real_early',json.dumps(early,ensure_ascii=False)));cur.execute('REPLACE INTO evaluation VALUES (%s,%s,UTC_TIMESTAMP())',('blind_real',json.dumps(result,ensure_ascii=False)));c.close();print('Recorded44/60; publication allowlist includes independently confirmed early and final cases')
if __name__=='__main__':main()
