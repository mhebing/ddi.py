from lxml.builder import ET

import pandas as pd


class DDI:
    """
    Base DDI class.
    """

    def __init__(self):
        self.meta = {}
        self.data = None

    def add_statistics(self):
        for varname, meta in self.meta.items():
            if varname in self.data:
                var = self.data[varname]
                self._add_frequencies(var, varname, meta)
                self._add_basic_statistics(var, varname, meta)

    def as_xml(self):
        doc = ET.Element("codebook")
        for varname, meta in self.meta.items():
            var = ET.SubElement(doc, "var")
            name = ET.SubElement(var, "name")
            name.text = meta["name"]
        return doc

    def _add_frequencies(self, var, varname, meta):
        if len(var.unique()) < 30:
            counts = dict(var.value_counts(dropna=False, sort=False))
            for x in counts.keys():
                e = counts.pop(x)
                try:
                    x = int(x)
                except:
                    pass
                counts[x] = e
            meta["frequencies"] = counts

    def _add_basic_statistics(self, var, varname, meta):
        statistics = dict(count=len(var), missing_cases=sum(pd.isnull(var)))
        statistics["valid_cases"] = statistics["count"] - statistics["missing_cases"]
        try:
            statistics["var"] = var.var()
            statistics["min"] = var.min()
            statistics["max"] = var.max()
        except:
            pass
        meta["statistics"] = statistics


class Variable:
    """
    Variable
    """

    def __init__(self, data, meta):
        self.data = data
        self.meta = meta
        self._set_attributes(meta)

    def as_xml(self, parent):
        xml = ET.SubElement(parent, id=self.name, sn=self.number)
        ET.SubElement(xml, "label").text = self.label
        cats = ET.SubElement(xml, "categories")
        for key, val in self.categories.items():
            ET.SubElement(cats, dict(id=key)).text = val

    def _set_attributes(self, meta):
        self.name = meta.get("name")
        self.label = meta.get("label")
        self.number = meta.get("number")
        self.categories = meta.get("value_labels")
        self.name = meta.get("name")
