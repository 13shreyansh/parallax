"""Intentional negative control on an unmerged CI proof branch only."""
import unittest

class CraciFailureProbe(unittest.TestCase):
    def test_a_regression_blocks_the_pipeline(self):
        self.assertEqual(1, 0, 'Intentional CI negative control; do not merge this branch')
