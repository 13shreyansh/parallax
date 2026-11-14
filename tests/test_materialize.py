import unittest
from pipeline.materialize_groups import versions_for
class Materialize(unittest.TestCase):
    def test_untranslated_retrieval_candidates_remain_readable(self):
        r={'id':'a','lang':'fi','section':'History','text':'Todellinen väite.','rev_id':1}
        v=versions_for({'anchor_id':'a','candidates':{'fi':[r]}})
        self.assertEqual(v['fi']['text'],r['text']);self.assertIsNone(v['fi']['gloss'])
