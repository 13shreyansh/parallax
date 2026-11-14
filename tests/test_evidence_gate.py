import unittest
from pipeline.check import valid_flag,attach_source

class Evidence(unittest.TestCase):
    def payload(self,status='Read'):
        return {'candidates':{'en':[{'id':'a','lang':'en','text':'It happened in 1940.','citations':[{'id':'s'}]}]},'sources':{'s':{'status':status,'passages':[{'text':'It happened in 1939.'}],'full_source_text':'It happened in 1939.'}},'second_pass':True}
    def flag(self):return {'check':'src','verdict':'Contradicted','language':'en','claim_id':'a','marks':{'a':['1940']},'source_id':'s','source_passage':'It happened in 1939.','source_marks':['1939'],'suggestion':None}
    def test_literal_contradiction_passes(self):self.assertTrue(valid_flag(self.flag(),self.payload()))
    def test_catalogue_is_not_a_read_book(self):self.assertFalse(valid_flag(self.flag(),self.payload('Book, not checked')))
    def test_fabricated_quote_is_rejected(self):
        f=self.flag();f['source_passage']='It happened in 1938.'
        self.assertFalse(valid_flag(f,self.payload()))
    def test_absence_requires_the_complete_article(self):
        f=self.flag();f.update(check='lang',verdict='Missing in Swedish',source_id=None,source_passage=None)
        self.assertFalse(valid_flag(f,self.payload()))
        p=self.payload();p['full_article_text']={'sv':'An entire different article.'}
        self.assertTrue(valid_flag(f,p))
    def test_language_result_with_unknown_source_id_does_not_crash_or_quote_it(self):
        f={'check':'lang','source_id':'not-retrieved','source_passage':'invented'}
        attach_source(f,{'sources':{}})
        self.assertIsNone(f['source_id']);self.assertNotIn('source',f)
