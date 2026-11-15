import unittest
from service.app import comparison_language
class InspectionAlignment(unittest.TestCase):
 def test_swedish_claim_is_compared_to_another_language(self):
  self.assertEqual(comparison_language('sv'),'fi')
  self.assertEqual(comparison_language('en'),'sv')
  self.assertEqual(comparison_language('fi'),'sv')
 def test_aligned_claims_panel_uses_the_displayed_pair(self):
  from service.app import shown_peers
  groups=[{'anchor_id':'x','versions':{'fi':{'id':'x'},'sv':{'id':'y'}}},{'anchor_id':'a','versions':{'fi':{'claim_id':'a'},'sv':{'claim_id':'b'},'en':{'claim_id':'c'}}}]
  self.assertEqual(shown_peers(groups,'a'),['b','c'])
  self.assertEqual(shown_peers(groups,'c'),['a','b'])
  self.assertEqual(shown_peers(groups,'zzz'),[])
