import os
import unittest

class TestTest(unittest.TestCase):
    def test_test(self):
        self.assertTrue(True)

    def test_path(self):
        """Correct path to testdata"""
        self.assertTrue(os.path.exists("test/data"))
