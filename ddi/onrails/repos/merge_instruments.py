"""
This module contains a set of fuctions to generate the JSON formats, as expected by DDI on Rails 2, from ``questions.csv`` and ``answers.csv``

The ``main()`` function execute the relevant methods in the correct order.
"""
import os
import json, glob
import yaml
from collections import defaultdict, OrderedDict
import pandas as pd


class InstrumentParser:
    """
    The InstrumentParser expects the following three inputs:
      
    -   ``questionnaires.csv``
    -   ``questions.csv``
    -   ``answers.csv``

    ``questions.csv`` and ``answers.csv`` can be used in two ways: either
    containing the information on all questionnaires in one file each or beeing
    nested in sub-directories (one for each instrument), e.g.::

        Option 1:
        metadata/answers.csv
        metadata/questions.csv

        Option 2:
        metadata/instruments/instrument_1/answers.csv
        metadata/instruments/instrument_1/questions.csv
        metadata/instruments/instrument_2/answers.csv
        metadata/instruments/instrument_2/questions.csv
        …

    To convert all input files to the corresponding JSON files, simply execute::

        InstrumentParser().run()
    """

    def __init__(self):
        """Init the InstrumentParser class."""
        pass

    def run(self, export_json=True, export_yaml=False):
        """
        Execute the parser.

        :param bool export_json: Write json files.
        :param bool export_yaml: Write xaml files.
        """
        tables = self._import_tables()
        answers = self._get_answers(tables)
        instruments = self._get_instruments(tables)
        self._fill_questions(tables, instruments, answers)
        self._export(instruments, export_json, export_yaml)
        return instruments
    
    def _read_tables(self, name):
        tables = glob.glob("metadata/*/*/%s" % name)
        tables += glob.glob("metadata/%s" % name)
        result = pd.read_csv(tables.pop())
        for table in tables:
            result = result.append(pd.read_csv(table))
        return result
    
    def _import_tables(self):
        tables = OrderedDict(
            questionnaires=pd.read_csv("metadata/questionnaires.csv"),
            questions=self._read_tables("questions.csv"),
            answers=self._read_tables("answers.csv"),
        )
        return tables
    
    def _get_answers(self, tables):
        answers = OrderedDict()
        for i, answer in tables["answers"].iterrows():
            answer = OrderedDict(answer.dropna())
            key = (answer["questionnaire"], answer["answer_list"])
            if not key in answers:
                answers[key] = list()
            self._clean_x(answer)
            answers[key].append(answer)
        return answers
    
    def _get_instruments(self, tables):
        instrument_list = [
            OrderedDict(row.dropna())
            for i, row
            in tables["questionnaires"].iterrows()
        ]
        instruments = OrderedDict([
            (x["questionnaire"], x)
            for x
            in instrument_list
        ])
        for instrument in instruments.values():
            instrument["instrument"] = instrument["questionnaire"]
            instrument["questions"] = OrderedDict()
        return instruments
    
    def _fill_questions(self, tables, instruments, answers):
        for i, item in tables["questions"].iterrows():
            item = OrderedDict(item.dropna())
            instrument_name = item["questionnaire"]
            question_name = item["question"]
            image_url = item.get("image_url", "")
            if "item" in item.keys():
                item_name = item["item"]
            else:
                item_name = "root"
            if not instrument_name in instruments:
                instruments[instrument_name] = OrderedDict(
                    instrument=instrument_name,
                    questions=OrderedDict(),
                )
            instrument_questions = instruments[instrument_name]["questions"]
            if not question_name in instrument_questions:
                question = OrderedDict()
                question["question"] = question_name
                question["name"] = question_name
                if not "label" in question and "text" in item:
                    question["label"] = item["text"]
                question["items"] = OrderedDict()
                question["image_url"] = image_url
                question["sn"] = len(instrument_questions)
                question["instrument"] = item["questionnaire"]
                question["study"] = item["study"]
                instrument_questions[question_name] = question
            question_items = instrument_questions[question_name]["items"]
            try:
                key = (item["questionnaire"], item["answer_list"])
                item["answers"] = answers[key]
            except:
                pass
            item["sn"] = len(question_items)
            self._clean_x(item)
            question_items[item_name] = item
        for iname, instrument in instruments.items():
            for qname, question in instrument["questions"].items():
                qitems = question["items"]
                for key, item in qitems.items():
                    item["item"] = str(key)
                    item["number"] = str(item.get("number", ""))
                    for k in [k for k in item.keys() if "." in k ]:
                        item.pop(k)
                question["items"] = list(qitems.values())
        return instruments
    
    def _clean_x(self, x):
        del(x["study"])
        del(x["questionnaire"])
        if "answer_list" in x and not "question" in x:
            del(x["answer_list"])
        if "question" in x:
            del(x["question"])
        return x
    
    def _write_json(self, instruments):
        os.system("rm -r ddionrails/instruments; mkdir -p ddionrails/instruments")
        for instrument_name, instrument in instruments.items():
            with open("ddionrails/instruments/%s.json" % instrument_name, "w") as f:
                json.dump(instrument, f, indent=2)
    
    def _write_yaml(self, instruments):
        os.system("rm -r temp/instruments; mkdir -p temp/instruments")
        for instrument_name, instrument in instruments.items():
            with open("temp/instruments/%s.yaml" % instrument_name, "w") as f:
                yaml.dump(instrument, f, default_flow_style=False)
    
    def _export(self, instruments, export_json=True, export_yaml=False):
        if export_json:
            self._write_json(instruments)
        if export_yaml:
            self._write_yaml(instruments)

def main(export_json=True, export_yaml=False):
    """
    DEPRECATED, please use the InstrumentParser directly::

        InstrumentParser().run()
    """
    instruments = InstrumentParser().run(export_json, export_yaml)
    return instruments

if __name__ == "__main__":
    instruments = main(export_yaml=True)
