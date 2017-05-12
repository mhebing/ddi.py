import re
import pandas as pd
import numpy as np
import os,sys, yaml, csv

sys.path.append(os.path.abspath("../../../ddi.py"))
from ddi.dataset import Dataset

def stata_to_statistics(study, input, output):
    filereader = pd.read_csv(input, delimiter=",", header = 0)

    for data, weight, split, analysis_unit, period, sub_type in zip(filereader.filename, filereader.weight, filereader.split, filereader.analysis_unit, filereader.period, filereader.sub_type):
        d1 = Dataset()
        try:
            d1.read_stata("../../../../data/soep/testdata/" + data + ".dta")
        except:
            print("Unable to find " + data + ".dta.")
            continue
        d1.write_tdp(output + data + ".csv", output + data + ".json")
        d1.write_stats(output + data + "_stats.json", split=split, weight=weight, analysis_unit=analysis_unit, period=period, sub_type=sub_type, study=study)
