from scipy.stats import gaussian_kde
from jinja2 import Template
import re, os
import json, yaml
import numpy as np
import pandas as pd
import collections
import math

cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

templatepath = cur_dir + "/convert/template_stats.html"
template_stats = "\"\"\"" + open(templatepath).read() + "\"\"\""
   
def uni_cat(elem, elem_de, file_csv, var_weight):

    frequencies = []
    values = []
    missings = []
    labels = []

    if elem_de!="":
        labels_de = []

        value_count = file_csv[elem["name"]].value_counts()
        for i, (value, value_de) in enumerate(zip(elem["values"], elem_de["values"])):
            try:
                frequencies.append(int(value_count[value["value"]]))
            except:
                frequencies.append(0)
            labels.append(value["label"])
            labels_de.append(value_de["label"])
            if value["value"]>=0:
                missings.append("false")
            else:
                missings.append("true")
            values.append(value["value"]) 
    else:
        value_count = file_csv[elem["name"]].value_counts()
        for i, value in enumerate(elem["values"]):
            try:
                frequencies.append(int(value_count[value["value"]]))
            except:
                frequencies.append(0)
            labels.append(value["label"])
            if value["value"]>=0:
                missings.append("false")
            else:
                missings.append("true")
            values.append(value["value"])
    '''
    missing_count = sum(i<0 for i in file_csv[elem["name"]])
    print(elem["name"])
    '''

    cat_dict = dict(
        frequencies = frequencies,
        values = values,
        missings = missings,
        labels = labels,
        )
    if elem_de!="":
        cat_dict["labels_de"]=labels_de
        
    # weighted
    weighted = []
    if var_weight != "":
        f_w = file_csv.pivot_table(index=elem["name"], values=var_weight, aggfunc=np.sum)
        for index, value in enumerate(elem["values"]):
            try:
                weighted.append(int(f_w[value["value"]]))
            except:
                weighted.append(0)
        cat_dict["weighted"] = weighted
    
    return cat_dict

def uni_string(elem, file_csv):
    frequencies = []
    missings = []

    len_unique = len(file_csv[elem["name"]].unique())
    len_missing = 0
    for i in file_csv[elem["name"]].unique():
        if "-1" in str(i):
            len_unique-=1
            len_missing+=1
        elif "-2" in str(i):
            len_unique-=1
            len_missing+=1
        elif "-3" in str(i):
            len_unique-=1
            len_missing+=1
        elif "nan" in str(i):
            len_unique-=1
            len_missing+=1
    frequencies.append(len_unique)
    missings.append(len_missing)


    string_dict = dict(
        frequencies = frequencies,
        missings = missings, #includes system missings
        )

    return string_dict

def uni_number(elem, file_csv, var_weight, num_density_elements=20):
    if file_csv[elem["name"]].dtype == "object" or file_csv[elem["name"]].dtype == "object":
        file_csv[elem["name"]] = pd.to_numeric(file_csv[elem["name"]])

    #missings        
    missings = dict(
        frequencies=[],
        labels=[],
        values=[],
    )
    
    density = []
    total = []
    valid = []
    missing = []

    # min and max
    try:
        min_val = min(i for i in file_csv[elem["name"]] if i>=0).astype(np.float64)
        max_val = max(i for i in file_csv[elem["name"]] if i>=0).astype(np.float64)

        # density          
        temp_array = []
        for num in file_csv[elem["name"]]:
            if num>=0:
                temp_array.append(float(num))
        density_range = np.linspace(min_val, max_val, num_density_elements)
        try:
            density_temp = gaussian_kde(sorted(temp_array)).evaluate(density_range)
            by = float(density_range[1]-density_range[0])
            density = density_temp.tolist()
        except:
            by = 0
            density = []

        # tranform to percentage
        '''
        x = sum(density)
        for i, c in enumerate(density):
            density[i] = density[i]/x
        '''
        
    except:
        min_val = []
        max_val = []
        by = 0
        density = []

    # missings
    for i in file_csv[elem["name"]].unique():
        if i<0:
            missings["frequencies"].append(file_csv[elem["name"]].value_counts()[i].astype(np.float64))
            missings["values"].append(float(i))
            # missings["labels"].append.... # there are no labels for missings in numeric variables 
    missing.append(sum(missings["frequencies"]))
    
    if var_weight != "" and elem["name"] != var_weight:
        weighted = []
        # weighted densities: difficult to calculate the weighted value f.e. wave with pivot
        '''
        try:
            f_w = file_csv.pivot_table(index=elem["name"], values=var_weight, aggfunc=np.sum)
            temp_array = []
            for num in f_w:
                if num>=0:
                    temp_array.append(float(num))
            density_temp = gaussian_kde(sorted(temp_array)).evaluate(density_range)
            weighted = density_temp.tolist()
        except:
            weighted = []
        '''

        # weighted missings
        missings["weighted"] = []
        f_w = file_csv.pivot_table(index=elem["name"], values=var_weight, aggfunc=np.sum)

        for i in missings["values"]:
            try:
                missings["weighted"].append(int(f_w[i]))
            except:
                missings["weighted"].append(0)
    
    # total and valid
    total = int(file_csv[elem["name"]].size)
    valid = total - int(file_csv[elem["name"]].isnull().sum())

    number_dict = dict(
        density = density,
        min = min_val,
        max = max_val,
        by = by,
        total = total,
        valid = valid,
        missing = missing,
        num_missings = missings,
        )
        
    if var_weight != "" and elem["name"] != var_weight:
        number_dict["weighted"] = weighted

    return number_dict

def uni(elem, elem_de, file_csv, var_weight):

    statistics = {}
    
    # weight variable is just one variable
   
    if elem["type"] == "cat":
        cat_dict = uni_cat(elem, elem_de, file_csv, var_weight)

        statistics.update(
            cat_dict
        )
    
    elif elem["type"] == "string":

        string_dict = uni_string(elem, file_csv)

        statistics.update(
            string_dict
        )
    
    elif elem["type"] == "number": 

        number_dict = uni_number(elem, file_csv, var_weight)

        statistics.update(
            number_dict
        )
    
    return statistics

def bi(base, elem, elem_de, scale, file_csv, file_json, split, weight):
    # split: variable for bi-variate analysis
    # base: variable for bi-variate analysis (every variable except split)
    categories = dict()

    for j, temp in enumerate(file_json["resources"][0]["schema"]["fields"]):
        if temp["name"] in split:
            s = temp["name"]
            bi = dict()
            bi[s] = dict()
            if temp["type"] == "number":
                list = map(float, file_csv[temp["name"]].unique())
            else:
                list = temp["values"]
            for index, value in enumerate(list):
                try:
                    v = value["value"]
                except:
                    v = int(value)
                temp_csv = file_csv.ix[file_csv[s] == v]
                categories[v] = uni(elem, elem_de, temp_csv, weight)
                try:
                    categories[v]["label"] = temp["values"][index]["label"]
                except:
                    categories[v]["label"] = v

                if elem["type"] == "cat":
                    uni_source = uni(elem, elem_de, temp_csv, weight)
                    for i in ["values", "missings", "labels"]:
                        bi[s][i] = uni_source[i]
                        del categories[v][i]

                elif elem["type"] == "number":
                    uni_source = uni(elem, elem_de, file_csv, weight)
                    for i in ["min", "max", "by"]:
                        bi[s][i] = uni_source[i]
                        del categories[v][i]

                categories = { str(key): value for key, value in categories.items() }
                ordered_categories = collections.OrderedDict(sorted(categories.items()))

            bi[s].update(dict(
                label = temp["label"],
                categories = ordered_categories,
                ))    

    return bi


def stat_dict(dataset_name, elem, elem_de, file_csv, file_json, file_de_json, split, weight, analysis_unit, period, sub_type, study):
    scale = elem["type"][0:3]
    
    if type(sub_type) == np.float64 and math.isnan(sub_type) == True:
        sub_type=""

    stat_dict = dict(
        study = study,
        analysis_unit = analysis_unit,
        period = str(period),
        sub_type = sub_type,
        dataset = file_json["name"].lower(),
        dataset_cs = file_json["name"],
        variable = elem["name"],
        name = elem["name"].lower(),
        name_cs = elem["name"],
        label = elem["label"],
        scale = scale,
        uni = uni(elem, elem_de, file_csv, weight),
        )
    if elem_de != "":
        stat_dict["label_de"] = elem_de["label"]

    if elem["name"] not in split and split!=[np.nan] and split!=[""] and str(split)!="[nan]":
        stat_dict["bi"] = bi(elem["name"], elem, elem_de, scale, file_csv, file_json, split, weight)

    return stat_dict

def generate_stat(dataset_name, d, m, m_de, vistest, split, weight, analysis_unit, period, sub_type, study):
    stat = []
    if m_de != "":
        for i, (elem, elem_de) in enumerate(zip(m["resources"][0]["schema"]["fields"], 
                                                m_de["resources"][0]["schema"]["fields"]
                                                )
        ):
            stat.append(
                stat_dict(dataset_name, elem, elem_de, d, m, m_de, split, 
                          weight, analysis_unit, period, sub_type, study
                )
            )
            if vistest!="":
                # Test for Visualization
                write_vistest(stat[-1], dataset_name, elem["name"], vistest)
    else:
        for i, elem in enumerate(m["resources"][0]["schema"]["fields"]):
            elem_de=""
            stat.append(
                stat_dict(dataset_name, elem, elem_de, d, m, m_de, split, 
                          weight, analysis_unit, period, sub_type, study
                )
            )
            if vistest!="":
                # Test for Visualization
                write_vistest(stat[-1], dataset_name, elem["name"], vistest)
                
    return stat
    
def write_vistest(stat, dataset_name, var_name, vistest):
    vistest_name = "".join((dataset_name, "_", var_name, ".json"))
    print("write \"" + vistest_name + "\" in \"" + vistest + "\"")
    if not os.path.exists(vistest):
        os.makedirs(vistest)
    with open("".join((vistest, vistest_name)), "w") as json_file:
        json.dump(stat, json_file, indent=2)
    
def write_stats(data, metadata, filename, file_type="json", split="", weight="", analysis_unit="", period="", sub_type="", study="", metadata_de="", vistest=""):
    dataset_name = re.search('^.*\/([^-]*)\..*$', filename).group(1)
    split = [split]
    stat = generate_stat(dataset_name, data, metadata, metadata_de, vistest, split, weight, analysis_unit, period, sub_type, study)
    if file_type == "json":
        print("write \"" + filename + "\"")    
        with open(filename, 'w') as json_file:
            json.dump(stat, json_file, indent=2)
    elif file_type == "yaml":
        print("write \"" + filename + "\"")
        with open(filename, 'w') as yaml_file:
            yaml_file.write(yaml.dump(stat, default_flow_style=False))
    elif file_type == "html":
        template = Template(template_stats)
        stats_html = template.render(
            stat=stat,
            )
        print("write \"" + filename + "\"")
        Html_file= open(filename,"w")
        Html_file.write(stats_html)
        Html_file.close()
    else:
        print("[ERROR] Unknown file type.")
