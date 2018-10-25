"""
This module supports studies, which already prepared metadata for the first
version of DDI on Rails. The functions in this module convert the input formats
from DDI on Rails (v1) to the input formats for DDI on Rails 2.

All studies are expected to use the new data formats. Therefore, all functions
in this module are DEPRECATED.
"""
import pandas as pd

def lower_all_names(x):
    """
    DEPRECATED

    Helper: Set all values in a dict to lowercase where the key includes
    "_name". DDI on Rails expects all name fields to be unique in their
    lowercase form.
    """
    def lower_x(x):
        try:
            return x.lower()
        except:
            return x
    names = [key for key in x.keys() if "_name" in key]
    x.ix[ : , names] = x.ix[ : , names].applymap(lower_x)

def datasets():
    """
    DEPRECATED

    Convert the version 1 ``logical_datasets.csv`` to the version 2
    ``datasets.csv``.
    """
    x = pd.read_csv("metadata/logical_datasets.csv")
    x.rename(columns={
        "study":"study_name",
        "dataset":"dataset_name",
        "period":"period_name",
        "analysis_unit":"analysis_unit_name",
        "conceptual_dataset":"conceptual_dataset_name",
    }, inplace=True)
    lower_all_names(x)
    x.to_csv("ddionrails/datasets.csv", index=False)

def variables():
    """
    DEPRECATED

    Convert the version 1 ``logical_variables.csv`` to the version 2
    ``variables.csv``.
    """
    x = pd.read_csv("metadata/logical_variables.csv")
    x.rename(columns={
        "study":"study_name",
        "dataset":"dataset_name",
        "variable":"variable_name",
        "concept":"concept_name",
    }, inplace=True)
    valid = x.ix[ : , (
        "study_name", "dataset_name", "variable_name",
        "label", "description", "description_long"
    )].duplicated() == False
    x = x.ix[valid]
    lower_all_names(x)
    x.to_csv("ddionrails/variables.csv", index=False)

def transformations():
    """
    DEPRECATED

    Convert the version 1 ``generations.csv`` to the version 2
    ``transformations.csv``.
    """
    x = pd.read_csv("metadata/generations.csv")
    x.rename(columns={
        "output_study":"target_study_name",
        "output_dataset":"target_dataset_name",
        "output_variable":"target_variable_name",
        "input_study":"origin_study_name",
        "input_dataset":"origin_dataset_name",
        "input_variable":"origin_variable_name",
    }, inplace=True)
    lower_all_names(x)
    x.to_csv("ddionrails/transformations.csv", index=False)

def questions_variables():
    """
    DEPRECATED

    Extract connections between questions and variables from the version 1
    ``logical_variables.csv`` and write them to the version 2
    ``questions_variables.csv``.
    """
    x = pd.read_csv("metadata/logical_variables.csv")
    x.rename(columns={
        "study":"study_name",
        "dataset":"dataset_name",
        "variable":"variable_name",
        "questionnaire":"instrument_name",
        "question":"question_name"
    }, inplace=True)
    x = x[["study_name", "dataset_name", "variable_name", "instrument_name",
        "question_name"]]
    x.dropna(axis=0, how="any", inplace=True)
    lower_all_names(x)
    x.to_csv("ddionrails/questions_variables.csv", index=False)

def concepts_questions():
    """
    DEPRECATED

    Extract connections between concepts and questions from the version 1
    ``questions.csv`` and write them to the version 2
    ``concepts_questions.csv``.
    """
    x = pd.read_csv("metadata/questions.csv")
    x.rename(columns={
        "study":"study_name",
        "questionnaire":"instrument_name",
        "question":"question_name",
        "concept":"concept_name",
    }, inplace=True)
    x = x[["study_name", "instrument_name", "question_name", "concept_name"]]
    x.dropna(axis=0, how="any", inplace=True)
    lower_all_names(x)
    x.to_csv("ddionrails/concepts_questions.csv", index=False)
