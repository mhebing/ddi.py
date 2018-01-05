# import re, os
import json, yaml
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def write_tdp(d, m, output_csv, output_json):

    logger.info("write \"" + output_csv + "\"")
    d.to_csv(output_csv, index=False)

    logger.info("write \"" + output_json + "\"")
    with open(output_json, "w") as json_file:
      json.dump(m, json_file, indent=2)
