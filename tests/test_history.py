import unittest
from pipeline.history import normalize

class History(unittest.TestCase):
    def test_short_footnotes_do_not_hide_the_wording_onset(self):
        self.assertEqual(normalize('The words!{{sfnp|Author|1991|p=12}} More words.'),'The words! More words.')
    def test_markup_and_comments_preserve_the_displayed_claim(self):
        self.assertEqual(normalize("It was [[Finland|Finnish]]<!-- hidden --> and ''neutral''.&nbsp;"),'It was Finnish and neutral.')
