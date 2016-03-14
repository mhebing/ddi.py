import pandas as pd

a = pd.read_stata("input/ah-raw.dta", index=["AHHNR"], order_categoricals=False)
b = pd.read_stata("input/bh-raw.dta", index=["BHHNR"], order_categoricals=False)
c = pd.read_stata("input/ch-raw.dta", index=["CHHNR"], order_categoricals=False)

ar = pd.read_stata("input/ah-raw.dta", iterator=True, convert_categoricals=False)

a_data = ar.read()
a_vars = [dict(name=var, sn=sn) for sn, var in enumerate(ar.varlist) ]

for sn, label in enumerate(ar.lbllist):
    label_dict = ar.value_labels()
    if label != "":
        a_vars[sn]["value_list"] = label
        a_vars[sn]["value_labels"] = label_dict[label]
    else:
        a_vars[sn]["value_list"] = None

for var in a_vars:
    var["label"] = ar.variable_labels()[var["name"]]

