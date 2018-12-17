import pandas as pd

from .ddi import DDI


class StataReader:
    """
    Basic reader for Stata files.

    Example::

        stata_reader = StataReader("data/test.dta")
        ddi = stata_reader.ddi
    """

    def __init__(self, path):
        """Init with a path to a Stata file."""
        self.file_format = "Stata"
        self.ddi = DDI()
        stata_file = self._open_stata_file(path)
        self.ddi.data = stata_file.read()
        self.ddi.meta = self._parse_meta(stata_file)
        stata_file.close()
        self._add_stata_data(path)

    def _open_stata_file(self, path):
        stata_file = pd.read_stata(
            path, convert_categoricals=False, order_categoricals=False, iterator=True
        )
        return stata_file

    def _parse_meta(self, stata_file):
        var_list = [dict(name=var, sn=sn) for sn, var in enumerate(stata_file.varlist)]

        for sn, label in enumerate(stata_file.lbllist):
            label_dict = stata_file.value_labels()
            if label != "":
                var_list[sn]["value_list"] = label
                var_list[sn]["value_labels"] = label_dict[label]
            else:
                var_list[sn]["value_list"] = None

        for var in var_list:
            var["label"] = stata_file.variable_labels()[var["name"]]
        return {var["name"]: var for var in var_list}

    def _add_stata_data(self, path):
        stata_file = self._open_stata_file(path)
        self.ddi.stata = stata_file.read(convert_missing=True)
        stata_file.close()


def read_stata(path):
    """
    Import Stata files.
    """
    ddi = StataReader(path).ddi
    return ddi
