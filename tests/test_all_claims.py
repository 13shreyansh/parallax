import unittest
from service.app import include_unrepresented
class AllClaims(unittest.TestCase):
    def test_a_peer_dropped_during_alignment_is_still_available_as_unchecked_text(self):
        groups=[{'id':'g','versions':{'en':{'claim_id':'a','text':'An English claim.'}}}]
        claims=[{'id':'a','lang':'en','ordinal':1},{'id':'b','lang':'fi','ordinal':2,'text':'Suomenkielinen väite.'}]
        out=include_unrepresented(groups,claims)
        self.assertEqual(len(out),2);self.assertEqual(out[1]['versions']['fi']['text'],claims[1]['text'])
        self.assertEqual(out[1]['checks']['state'],'pending');self.assertEqual(out[1]['flags'],[])
