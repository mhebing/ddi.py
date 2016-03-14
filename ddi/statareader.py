import pandas as pd
import numpy as np
from .ddi import DDI

def read_stata(path):
    """
    Import Stata files.
    """
    stata = pd.read_stata(
        path,
        convert_categoricals=False,
        order_categoricals=False,
        iterator=True,
    )
    ddi = DDI()
    ddi.data = stata.read()
    ########################################
    var_list = [dict(name=var, sn=sn) for sn, var in enumerate(stata.varlist) ]
    
    for sn, label in enumerate(stata.lbllist):
        label_dict = stata.value_labels()
        if label != "":
            var_list[sn]["value_list"] = label
            var_list[sn]["value_labels"] = label_dict[label]
        else:
            var_list[sn]["value_list"] = None
    
    for var in var_list:
        var["label"] = stata.variable_labels()[var["name"]]
    ########################################
    ddi.metadata = {
        var["name"]: var for var in var_list
    }
    return ddi
