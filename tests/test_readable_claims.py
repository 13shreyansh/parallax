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
