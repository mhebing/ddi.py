from ddi.convert.read_tdp import read_tdp
from ddi.convert.read_stata import read_stata
from ddi.convert.write_stats import write_stats
from ddi.convert.write_tdp import write_tdp
from ddi.convert.write_stata import write_stata
from ddi.tests.test_values import *
import unittest

class Dataset:

    def __init__(self):
        self.dataset = None
        self.metadata = None
        
    def read_tdp(self, csv_name, json_name):
        self.dataset, self.metadata = read_tdp(csv_name, json_name)
        
    def read_stata(self, dta_name):
        self.dataset, self.metadata = read_stata(dta_name)
    
    def write_stats(self, output_name, file_type="json"):
        write_stats(self.dataset, self.metadata, output_name, file_type=file_type)
        
    def write_tdp(self, output_csv, output_json):
        write_tdp(self.dataset, self.metadata, output_csv, output_json)
        
    def write_stata(self, output_name):
        write_stata(self.dataset, self.metadata, output_name)
        
    def test(self):
        y = [
            test_a_unique,
            test_b_uniqueid_notnull,
            test_c_validage,
            test_d_validsex,
        ]
        for x in y:
            try:
                x(self.dataset, self.metadata)
            except AssertionError as error:
                print("[ERROR]", error)

