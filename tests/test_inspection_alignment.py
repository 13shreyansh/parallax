import unittest
from service.app import comparison_language
class InspectionAlignment(unittest.TestCase):
 def test_swedish_claim_is_compared_to_another_language(self):
  self.assertEqual(comparison_language('sv'),'fi')
  self.assertEqual(comparison_language('en'),'sv')
  self.assertEqual(comparison_language('fi'),'sv')
