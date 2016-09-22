from ddi.convert.read_tdp import read_tdp
from ddi.convert.read_stata import read_stata
from ddi.convert.write_stats import write_stats
from ddi.convert.write_tdp import write_tdp
from ddi.convert.write_stata import write_stata

class Dataset:

    def __init__(self):
        self.dataset = None
        self.metadata = None
        
    def read_tdp(self, csv_name, json_name):
        self.dataset, self.metadata = read_tdp(csv_name, json_name)
    
    def write_stats(self, json_name, file_type="json"):
        write_stats(self.dataset, self.metadata, json_name, file_type=file_type)
