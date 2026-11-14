import unittest
from unittest.mock import patch,MagicMock
from pipeline.check import build_groups,evidence

class Cursor:
    def execute(self,sql,args=()):
        self.sql=sql
    def fetchall(self):
        if 'FROM article' in self.sql:return [{'lang':'fi'},{'lang':'en'}]
        if 'ORDER BY FIELD' in self.sql:return [{'id':'claim-a','lang':'fi','text':'A real statement.','ordinal':0}]
        return []
class Connection:
    def cursor(self):return Cursor()
    def close(self):pass
class Alignment(unittest.TestCase):
    def test_an_empty_existing_language_is_kept_for_omission_checks(self):
        with patch('pipeline.check.db',return_value=Connection()):
            groups=build_groups('Q-test')
        self.assertIn('en',groups[0]['candidates'])
        self.assertEqual(groups[0]['candidates']['en'],[])

    def test_empty_article_text_is_evidence_of_an_existing_empty_version(self):
        conn=MagicMock();cursor=conn.cursor.return_value
        cursor.fetchall.return_value=[];cursor.fetchone.return_value={'wikitext':''}
        row={'id':'a','lang':'fi','section':'History','text':'A real statement.','rev_id':1,'citations':'[]'}
        group={'id':'g','qid':'Q-test','anchor_id':'a','candidates':{'fi':[row],'en':[]}}
        with patch('pipeline.check.db',return_value=conn):payload=evidence(group)
        self.assertIn('en',payload['full_article_text'])
        self.assertEqual(payload['full_article_text']['en'],'')
