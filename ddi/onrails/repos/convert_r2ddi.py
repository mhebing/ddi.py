import glob, re, json, os
import yaml
from collections import defaultdict, OrderedDict
from lxml import etree

class Parser:

    def __init__(self, r2ddi_path="r2ddi", version = "v1", primary_language="en"):
        """
        The path must refer to the version, not to the language!

        good: "r2ddi/v1"

        bad: "r2ddi/v1/en"
        """
        self.path = r2ddi_path
        self.version = version
        self.primary_language = primary_language
        self.datasets = defaultdict(OrderedDict)
        self.run()

    def run(self):
        primary_names = set(glob.glob(os.path.join(
            self.path, self.version, self.primary_language, "*.xml",
        )))
        secondary_names = set(glob.glob(os.path.join(
            self.path, self.version, "*", "*.xml"
        ))).intersection(primary_names)
        for file_name in primary_names:
            print(file_name)
            self._parse_xml_file(file_name)

    def _parse_xml_file(self, path):
        xml_content = etree.parse(path)
        for xml_var in xml_content.findall("//var"):
            self._parse_xml_var(xml_var)

    def _parse_xml_var(self, xml_var):
        dataset = xml_var.get("files").lower()
        variable = xml_var.get("ID").lower()
        var_dict = dict(
            name=variable,
            name_cs=xml_var.get("ID"),
            variable=variable,
            dataset=dataset,
            label=xml_var.findtext("labl"),
            categories=self._get_categories(xml_var),
            statistics=self._get_statistics(xml_var),
        )
        if xml_var.get("intrvl") == "labeled_numeric":
            var_dict["scale"] = "cat"
        else:
            var_dict["scale"] = ""
        self.datasets[dataset][variable] = var_dict

    def _get_categories(self, xml_var):
        result = dict(
            frequencies=[],
            labels=[],
            missings=[],
            values=[],
        )
        for xml_cat in xml_var.findall("catgry"):
            try:
                result["frequencies"].append(int(xml_cat.findtext("catStat")))
            except:
                result["frequencies"].append(int(0))
            result["labels"].append(xml_cat.findtext("labl"))
            if xml_cat.get("missing", "").lower() == "true":
                result["missings"].append(True)
            else:
                result["missings"].append(False)
            result["values"].append(xml_cat.findtext("catValu"))
        return result

    def _get_statistics(self, xml_var):
        result = dict(
            names=[],
            values=[],
        )
        for xml_stat in xml_var.findall("sumStat"):
            result["names"].append(xml_stat.get("type"))
            result["values"].append(xml_stat.text)
        return result

    def write_json(self):
        with open("ddionrails/datasets.json", "w") as f:
            json.dump(self.datasets, f)

    def write_yaml(self):
        with open("ddionrails/datasets.yaml", "w") as f:
            yaml.dump(self.datasets, f, default_flow_style=False)
        
