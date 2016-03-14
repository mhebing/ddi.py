import os
import unittest
import pandas
from ddi import statareader

class TestStataReader(unittest.TestCase):

    def test_read_stata(self):
        self.assertEqual(
            statareader.read_stata("test/data/test1.dta").__class__,
            pandas.core.frame.DataFrame
        )
