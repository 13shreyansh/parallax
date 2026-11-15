import unittest
from service.app import source_title
class SourceTitle(unittest.TestCase):
    def test_missing_document_title_is_a_traceable_domain_label(self):
        self.assertEqual(source_title('untitled','https://www.example.org/paper.pdf'),'Source at example.org')
    def test_real_document_title_is_preserved(self):
        self.assertEqual(source_title('A real title','https://example.org'),'A real title')
