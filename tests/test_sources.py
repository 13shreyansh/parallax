import unittest
from unittest.mock import patch,Mock
from pipeline.sources import read_url

class Sources(unittest.TestCase):
    def test_html_meta_encoding_preserves_swedish_words(self):
        response=Mock(status_code=200,is_redirect=False,headers={'content-type':'text/html'},encoding='ISO-8859-1')
        response.iter_content.return_value=[('<html><meta charset="utf-8"><title>Historia</title><body><article><p>'+('Svenska frivilliga återvände från vinterkriget. '*15)+'</p></article></body></html>').encode()]
        with patch('pipeline.sources.public_url',return_value=True),patch('pipeline.sources.requests.get',return_value=response):
            result=read_url('https://example.org')
        self.assertIn('återvände',result['text'])
        self.assertNotIn('Ã',result['text'])
