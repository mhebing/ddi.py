# import re, os
import json, yaml
import numpy as np
import pandas as pd

def write_tdp(d, m, output_csv, output_json):

    d.to_csv(output_csv)

    with open(output_json, "w") as json_file:
      json.dump(m, json_file)
