import unittest
from pipeline.text import HistoricalIndex
class HistoricalTemplateSafety(unittest.TestCase):
 def test_missing_template_numbers_never_become_a_quote(self):
  self.assertIsNone(HistoricalIndex('The troops advanced {{convert|10|to|15|km}} past the defensive line.').match('The troops advanced 10 to past the defensive line.'))
 def test_unknown_inline_templates_do_not_silently_disappear(self):
  self.assertIsNone(HistoricalIndex('Over {{formatnum:24000}} veterans received their awards.').match('Over veterans received their awards.'))
 def test_plain_historical_words_still_match(self):
  quote='The equipment often could not withstand severe frost.'
  self.assertEqual(HistoricalIndex(quote).match(quote),quote)
