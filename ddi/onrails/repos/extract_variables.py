import glob
import os
import re

from lxml import etree

import pandas as pd

GIP_RE = re.compile(r"([a-z]{2})(\d{2})")


class XmlParser:
    def __init__(
        self,
        xml_path,
        study_name,
        write_variables=True,
        write_datasets=True,
        write_concepts=True,
    ):
        self.study = study_name
        self.write_variables = write_variables
        self.write_datasets = write_datasets
        self.write_concepts = write_concepts
        self.path = xml_path
        self.variables = list()
        self.datasets = list()
        self.concepts = list()

    def _parse_xml_file(self, path):
        xml_content = etree.parse(path)
        for xml_var in xml_content.findall("//var"):
            self._parse_xml_variable(xml_var)

    def _parse_xml_variable(self, xml_var):
        dataset = xml_var.get("files").lower()
        variable = xml_var.get("ID").lower()
        concept = variable
        if self.study == "gip":
            concept = GIP_RE.sub("\\1", concept)
        self.variables.append(
            dict(
                study_name=self.study,
                dataset_name=dataset,
                variable_name=variable,
                concept_namespace=self.study,
                concept_name=concept,
            )
        )
        self.datasets.append(dict(study_name=self.study, dataset_name=dataset))
        self.concepts.append(dict(concept_namespace=self.study, concept_name=concept))

    def _csv_helper(self, file_name, content):
        data = pd.DataFrame(content).drop_duplicates()
        data.to_csv(file_name, index=False)

    def _write_csv_files(self):
        if self.write_variables:
            self._csv_helper("ddionrails/variables.csv", self.variables)
        if self.write_datasets:
            self._csv_helper("ddionrails/datasets.csv", self.datasets)
        if self.write_concepts:
            self._csv_helper("ddionrails/concepts.csv", self.concepts)

    def run(self):
        xml_files = glob.glob(os.path.join(self.path, "*.xml"))
        for xml_file in xml_files:
            self._parse_xml_file(xml_file)
        self._write_csv_files()
