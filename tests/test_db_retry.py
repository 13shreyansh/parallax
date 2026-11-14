import unittest
from unittest.mock import patch
import pymysql
from pipeline.common import RetryingCursor,db

class Retry(unittest.TestCase):
    def test_vector_index_deadlock_retries_idempotent_statement(self):
        with patch.object(pymysql.cursors.DictCursor,'execute',side_effect=[pymysql.err.OperationalError(1213,'deadlock'),1]) as run,patch('pipeline.common.time.sleep'):
            cursor=RetryingCursor(None)
            self.assertEqual(cursor.execute('SELECT 1'),1)
            self.assertEqual(run.call_count,2)
    def test_authentication_errors_are_not_retried(self):
        with patch.object(pymysql.cursors.DictCursor,'execute',side_effect=pymysql.err.OperationalError(1045,'denied')) as run:
            with self.assertRaises(pymysql.err.OperationalError):RetryingCursor(None).execute('SELECT 1')
            self.assertEqual(run.call_count,1)
    def test_unix_socket_uses_the_hosted_reader_credential(self):
        with patch.dict('os.environ',{'PARALLAX_DB_USER':'parallax_read','PARALLAX_DB_PASSWORD':'fixture-value','PARALLAX_DB_SOCKET':'/run/mysqld/mysqld.sock'},clear=True),patch('pipeline.common.pymysql.connect') as connect:
            db()
            self.assertEqual(connect.call_args.kwargs['password'],'fixture-value')
            self.assertEqual(connect.call_args.kwargs['unix_socket'],'/run/mysqld/mysqld.sock')
