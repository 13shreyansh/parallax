import unittest
from service.app import temporal_query
class TemporalLookup(unittest.TestCase):
    def test_every_temporal_branch_uses_the_versioned_primary_key(self):
        sql,args=temporal_query([{'lang':'fi','page_id':12},{'lang':'sv','page_id':34}],'2012-11-27 23:59:59')
        self.assertEqual(sql.count('FOR SYSTEM_TIME AS OF TIMESTAMP'),2)
        self.assertEqual(sql.count('WHERE lang=%s AND page_id=%s'),2)
        self.assertNotIn('WHERE qid=',sql)
        self.assertEqual(args,('2012-11-27 23:59:59','fi',12,'2012-11-27 23:59:59','sv',34))
