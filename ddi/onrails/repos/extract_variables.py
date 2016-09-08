import os, sys, glob
import pandas as pd
import csv
from lxml import etree

class XmlParser:

    def __init__(self, xml_path, study_name):
        self.study = study_name
        self.path = xml_path
        self.variables = list()
        self.datasets = list()
        self.concepts = list()

    def _parse_xml_file(self, path):
        xml_content = etree.parse(path)
        for xml_var in xml_content.findall("//var"):
            self._parse_xml_variable(xml_var)
    
    def _parse_xml_variable(self, xml_var):
        dataset = xml_var.get("files")
        variable = xml_var.get("ID")
        self.variables.append(dict(
            study=self.study,
            dataset=dataset,
            variable=variable,
            concept=variable,
        ))
        self.datasets.append(dict(
            study=self.study,
            dataset=dataset,
        ))
        self.concepts.append(dict(
            namespace=self.study,
            concept=variable,
        ))

    def _csv_helper(self, file_name, content):
        data = pd.DataFrame(content).drop_duplicates()
        data.to_csv(file_name, index=False)
    
    def _write_csv_files(self):
        self._csv_helper("ddionrails/variables.csv", self.variables)
        self._csv_helper("ddionrails/datasets.csv", self.datasets)
        self._csv_helper("ddionrails/concepts.csv", self.concepts)

    def run(self):
        xml_files = glob.glob(os.path.join(self.path, "*.xml"))
        for xml_file in xml_files:
            self._parse_xml_file(xml_file)
        self._write_csv_files()
