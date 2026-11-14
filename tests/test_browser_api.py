import os,unittest
from unittest.mock import patch
from service.app import app
class BrowserApi(unittest.TestCase):
    def test_only_public_modes_are_dispatched(self):
        with patch.dict(os.environ,{'PARALLAX_BRIDGE_TOKEN':'fixture-secret'}),app.test_client() as client:
            self.assertEqual(client.get('/api/parallax?mode=__dict__').status_code,405)
            self.assertEqual(client.get('/api/parallax?mode=review').status_code,405)
            self.assertEqual(client.get('/home').status_code,403)
    def test_public_bridge_can_read_without_exposing_the_secret(self):
        with patch.dict(os.environ,{'PARALLAX_BRIDGE_TOKEN':'fixture-secret'}),patch.dict(app.view_functions,{'home':lambda:{'articles':[]}}),app.test_client() as client:
            response=client.get('/api/parallax?mode=home')
            self.assertEqual(response.status_code,200)
            self.assertNotIn('fixture-secret',response.get_data(as_text=True))
            self.assertEqual(response.headers['Cache-Control'],'no-store')
