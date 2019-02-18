import pandas as pd


def lower_all_names(x):
    def lower_x(x):
        try:
            return x.lower()
        except:
            return x

    names = [key for key in x.keys() if "_name" in key]
    x.ix[:, names] = x.ix[:, names].applymap(lower_x)


def datasets():
    x = pd.read_csv("metadata/logical_datasets.csv")
    x.rename(
        columns={
            "study": "study_name",
            "dataset": "dataset_name",
            "period": "period_name",
            "analysis_unit": "analysis_unit_name",
            "conceptual_dataset": "conceptual_dataset_name",
        },
        inplace=True,
    )
    lower_all_names(x)
    x.to_csv("ddionrails/datasets.csv", index=False)


def variables():
    x = pd.read_csv("metadata/logical_variables.csv")
    x.rename(
        columns={
            "study": "study_name",
            "dataset": "dataset_name",
            "variable": "variable_name",
            "concept": "concept_name",
        },
        inplace=True,
    )
    valid = (
        x.ix[
            :,
            (
                "study_name",
                "dataset_name",
                "variable_name",
                "label",
                "description",
                "description_long",
            ),
        ].duplicated()
        == False
    )
    x = x.ix[valid]
    lower_all_names(x)
    x.to_csv("ddionrails/variables.csv", index=False)


def transformations():
    x = pd.read_csv("metadata/generations.csv")
    x.rename(
        columns={
            "output_study": "target_study_name",
            "output_dataset": "target_dataset_name",
            "output_variable": "target_variable_name",
            "input_study": "origin_study_name",
            "input_dataset": "origin_dataset_name",
            "input_variable": "origin_variable_name",
        },
        inplace=True,
    )
    lower_all_names(x)
    x.to_csv("ddionrails/transformations.csv", index=False)


def questions_variables():
    x = pd.read_csv("metadata/logical_variables.csv")
    x.rename(
        columns={
            "study": "study_name",
            "dataset": "dataset_name",
            "variable": "variable_name",
            "questionnaire": "instrument_name",
            "question": "question_name",
        },
        inplace=True,
    )
    x = x[
        [
            "study_name",
            "dataset_name",
            "variable_name",
            "instrument_name",
            "question_name",
        ]
    ]
    x.dropna(axis=0, how="any", inplace=True)
    lower_all_names(x)
    x.to_csv("ddionrails/questions_variables.csv", index=False)


def concepts_questions():
    x = pd.read_csv("metadata/questions.csv")
    x.rename(
        columns={
            "study": "study_name",
            "questionnaire": "instrument_name",
            "question": "question_name",
            "concept": "concept_name",
        },
        inplace=True,
    )
    x = x[["study_name", "instrument_name", "question_name", "concept_name"]]
    x.dropna(axis=0, how="any", inplace=True)
    lower_all_names(x)
    x.to_csv("ddionrails/concepts_questions.csv", index=False)
