import re, os
import json, yaml
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def read_tdp(csv_file_name, json_file_name):
    logger.info("read \"" + csv_file_name + "\" and \"" + json_file_name + "\"")
    d = pd.read_csv(csv_file_name, index_col=None)
    #replace all stata missings (. and .a etc.) with NaN
    try:
        d = d.replace({"^\.\D?$":np.nan}, regex=True)
    except:
        pass
    with open(json_file_name) as json_file:
        metadata = json_file.read()
    m = json.loads(metadata)
    return d, m
