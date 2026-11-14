import unittest
from pipeline.extract import split_claims

class Claims(unittest.TestCase):
    def article(self,text):return {'qid':'Q1','lang':'en','rev_id':1,'wikitext':text}
    def test_trailing_reference_stays_on_previous_sentence(self):
        cs=split_claims(self.article('The first statement has more than thirty five characters.<ref>https://example.org/one</ref> The second statement also has more than thirty five characters.'))
        self.assertEqual(len(cs),2)
        self.assertEqual(cs[0]['citations'][0]['urls'],['https://example.org/one'])
        self.assertEqual(cs[1]['citations'],[])
    def test_named_reuse_resolves_definition_after_use(self):
        cs=split_claims(self.article('The first statement has more than thirty five characters.<ref name="one"/>\nThe second statement has more than thirty five characters.<ref name="one">{{cite web|url=https://example.org|title=Source}}</ref>'))
        self.assertEqual(cs[0]['citations'][0]['id'],cs[1]['citations'][0]['id'])
    def test_offline_book_is_not_a_source_failure_flag(self):
        cs=split_claims(self.article('The statement has more than thirty five characters.<ref>{{cite book|title=Historical book|isbn=123}}</ref>'))
        self.assertEqual(cs[0]['citations'][0]['status'],'Book, not checked')
    def test_short_footnote_is_preserved_as_offline_citation(self):
        cs=split_claims(self.article('The statement has more than thirty five characters.{{sfn|Trotter|1991|p=20}}'))
        self.assertEqual(cs[0]['citations'][0]['label'],'Trotter, 1991')
    def test_multiline_editor_comments_never_become_claims(self):
        cs=split_claims(self.article('The statement has more than thirty five characters. <!-- Hidden editor instructions\nThis invisible instruction is more than thirty five characters.\n-->'))
        self.assertEqual(len(cs),1)
        self.assertNotIn('Hidden',cs[0]['text'])
    def test_paragraph_ending_citation_keeps_its_scope(self):
        cs=split_claims(self.article('This earlier sentence has enough characters for the test. This later sentence ends with the paragraph reference.<ref>https://example.org</ref>'))
        self.assertEqual(cs[0]['citations'][0]['citation_scope'],'paragraph-ending')
        self.assertEqual(cs[1]['citations'][0]['citation_scope'],'sentence')

if __name__=='__main__':unittest.main()
