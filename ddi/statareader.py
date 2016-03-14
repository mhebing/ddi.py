import pandas as pd
import numpy as np

def read_stata(path):
    """
    Import Stata files.
    """
    data = pd.read_stata(path)
    return data
