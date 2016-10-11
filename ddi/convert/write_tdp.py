# import re, os
import json, yaml
import numpy as np
import pandas as pd

def write_tdp(d, m, output_csv, output_json):

    print("write \"" + output_csv + "\"")
    d.to_csv(output_csv)

    print("write \"" + output_json + "\"")
    with open(output_json, "w") as json_file:
      json.dump(m, json_file, indent=2)
