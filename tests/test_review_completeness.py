import unittest
from pipeline.record_final_review import UNCONFIRMED,REASONS
class BlindReviewCompleteness(unittest.TestCase):
    def test_every_randomly_selected_case_has_one_recorded_assessment(self):
        self.assertEqual(set(UNCONFIRMED)|set(REASONS),set(range(1,61)))
        self.assertFalse(set(UNCONFIRMED)&set(REASONS))
        self.assertEqual(len(REASONS),44)
        self.assertEqual(sum(x[0] is False for x in UNCONFIRMED.values()),13)
        self.assertEqual(sum(x[0] is None for x in UNCONFIRMED.values()),3)
