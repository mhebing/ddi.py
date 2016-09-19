import json, glob
import yaml
from collections import defaultdict, OrderedDict
import pandas as pd

def read_tables(name):
    tables = glob.glob("metadata/*/*/%s" % name)
    tables += glob.glob("metadata/%s" % name)
    result = pd.read_csv(tables.pop())
    for table in tables:
        result = result.append(pd.read_csv(table))
    return result

def import_tables():
    tables = OrderedDict(
        questionnaires=pd.read_csv("metadata/questionnaires.csv"),
        questions=read_tables("questions.csv"),
        answers=read_tables("answers.csv"),
    )
    return tables

def get_answers(tables):
    answers = OrderedDict()
    for i, answer in tables["answers"].iterrows():
        answer = OrderedDict(answer.dropna())
        key = (answer["questionnaire"], answer["answer_list"])
        if not key in answers:
            answers[key] = list()
        _clean_x(answer)
        answers[key].append(answer)
    return answers

def get_instruments(tables):
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

def fill_questions(tables, instruments, answers):
    for i, item in tables["questions"].iterrows():
        item = OrderedDict(item.dropna())
        instrument_name = item["questionnaire"]
        question_name = item["question"]
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
            if not "label" in question and "text" in question:
                question["label"] = item["text"]
            question["items"] = OrderedDict()
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
        _clean_x(item)
        question_items[item_name] = item
    return instruments

def _clean_x(x):
    del(x["study"])
    del(x["questionnaire"])
    if "answer_list" in x and not "question" in x:
        del(x["answer_list"])
    if "question" in x:
        del(x["question"])
    return x

def export(instruments, export_json=True, export_yaml=False):
    if export_json:
        with open("ddionrails/instruments.json", "w") as f:
            json.dump(instruments, f)
    if export_yaml:
        with open("ddionrails/instruments.yaml", "w") as f:
            yaml.dump(instruments, f, default_flow_style=False)

def main(export_json=True, export_yaml=False):
    tables = import_tables()
    answers = get_answers(tables)
    instruments = get_instruments(tables)
    fill_questions(tables, instruments, answers)
    export(instruments, export_json, export_yaml)
    return instruments

if __name__ == "__main__":
    instruments = main(export_yaml=True)
