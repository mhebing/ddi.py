import re, os
import json, yaml
import numpy as np
import pandas as pd

def read_tdp(csv_file_name, json_file_name):
    d = pd.read_csv(csv_file_name)
    with open(json_file_name) as json_file:
        metadata = json_file.read()
    m = json.loads(metadata)
    return d, m
