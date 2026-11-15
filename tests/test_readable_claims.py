import unittest
from pipeline.presentation import readable,readable_groups
class ReadableClaims(unittest.TestCase):
 def test_extraction_fragments_never_reach_readings(self):
  for text in ['thumb|Финский танк','mini|caption','{{Kirjaviite|Nimeke=test}}','[[File:test.jpg]]']:
   self.assertFalse(readable(text))
  self.assertTrue(readable('Cirka 9 500 svenska frivilliga deltog i vinterkriget.'))
 def test_clean_languages_survive_without_changing_quotes(self):
  g={'id':'a','versions':{'en':{'text':'A real claim.'},'ru':{'text':'thumb|caption'}}}
  result=readable_groups([g]);self.assertEqual(result[0]['versions'],{'en':{'text':'A real claim.'}})
  self.assertEqual(g['versions']['ru']['text'],'thumb|caption')

 def test_plain_text_with_dropped_template_values_requires_rendered_proof(self):
  g={'id':'a','versions':{'en':{'claim_id':'bad','text':'The army advanced 10 to past the line.'},'fi':{'claim_id':'good','text':'The complete verified sentence.'}}}
  self.assertEqual(set(readable_groups([g],{'good'})[0]['versions']),{'fi'})
