from scipy.stats import gaussian_kde
from jinja2 import Template
import re, os
import json, yaml
import numpy as np
import pandas as pd
    
template_stats="""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <title>Statistics {{stat[0]["dataset"]}}</title>
    </head>
    <body>
        <header>
            <h1>Statistics for Dataset {{stat[0]["dataset"]}}</h1>
        </header>
        <main>
            {% for var in stat %}
                <h2>{{var["variable"]}}</h2>
                <table class="table table-striped" style="width: 25%;">
                    <tr>
                        <td>variable name:</td>
                        <td>{{var["variable"]}}</td>
                    </tr>
                    <tr>
                        <td>variable label:</td>
                        <td>{{var["label"]}}</td>
                    </tr>
                    <tr>
                        <td>scale:</td>
                        <td>{{var["scale"]}}</td>
                    </tr>
                    <tr>
                        <td>study:</td>
                        <td>{{var["study"]}}</td>
                    </tr>
                    <tr>
                        <td>dataset:</td>
                        <td>{{var["dataset"]}}</td>
                    </tr>
                </table>
                
                
                {% if var["scale"] == "cat" %}
                    <h3>Univariate Statistics</h3>
                    <table class="table table-striped" style="width: 50%;">
                        <thead>
                            <tr>
                                <th>Value Labels</th>
                                <th>Values</th>
                                <th>Missings</th>
                                <th>Frequencies</th>
                                {% if var["uni"]["weighted"] is defined %}
                                    <th>Weighted Frequencies</th>
                                {% endif %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for i in range(var["uni"]["frequencies"]|length) %}
                                <tr>
                                    <td>{{var["uni"]["labels"][i]}}</td>
                                    <td>{{var["uni"]["values"][i]}}</td>
                                    <td>{{var["uni"]["missings"][i]}}</td>
                                    <td>{{var["uni"]["frequencies"][i]}}</td>
                                    {% if var["uni"]["weighted"] is defined %}
                                        <td>{{var["uni"]["weighted"][i]}}</td>
                                    {% endif %}
                                </tr>
                            {% endfor %} 
                        </tbody>
                    </table>
                    <h3>Bivariate Statistics</h3>
                {% endif %}
                
                
                {% if var["scale"] == "str" %}
                    <h3>Univariate Statistics</h3>
                    <table>
                        <tr>
                            <td>Frequencies:</td>
                            <td>{{var["uni"]["frequencies"][0]}}</td>
                        </tr>
                        <tr>
                            <td>Missings:</td>
                            <td>{{var["uni"]["missings"][0]}}</td>
                        </tr>
                    </table>
                {% endif %}
                
                {% if var["scale"] == "num" %}
                    <h3>Univariate Statistics</h3>
                    <table>
                        <tr>
                            <td>Minimum:</td>
                            <td>{{var["uni"]["min"]}}</td>
                        </tr>
                        <tr>
                            <td>Maximum:</td>
                            <td>{{var["uni"]["max"]}}</td>
                        </tr>
                        <tr>
                            <td>Valid:</td>
                            <td>{{var["uni"]["valid"]}}</td>
                        </tr>
                        <tr>
                            <td>Missings:</td>
                            <td>{{var["uni"]["missing"][0]}}</td>
                        </tr>
                    </table>
                {% endif %}
                <hr />
            {% endfor %}         
        </main>
    </body>
</html>
"""    

def get_missing_codes():
    missing_index = [0,1,2]
    missing_value = [-3,-2,-1]
    missing_label = ["nicht valide", "trifft nicht zu", "keine Angabe"]

    return missing_index, missing_value, missing_label

def get_dataframes(elem, file_csv):
    #create df without missings    
    df_nomis = file_csv[elem["name"]].copy()
    
    #create df with only missings
    df_mis = file_csv[elem["name"]].copy()

    for index, value in enumerate(df_nomis):
        try:
            if int(value) < 0: 
                df_nomis[index] = np.nan
        except:
            pass
 
    for index, value in enumerate(df_mis):
        try:
            if int(value) >= 0:
                df_mis[index] = np.nan
        except:
            pass

    return df_nomis, df_mis
   
def uni_cat(elem, file_csv, var_weight):

    frequencies = []
    values = []
    missings = []
    labels = []

    value_count = file_csv[elem["name"]].value_counts()
    for index, value in enumerate(elem["values"]):
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
    
    if var_weight != "":
        weighted = []
        # weighted placeholder
        weighted = density[:]
        
        # weighted missings
        if elem["name"] != var_weight:
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
        missings = missings,
        )
        
    if var_weight != "":
        number_dict["weighted"] = weighted

    return number_dict

def uni(elem, scale, file_csv, file_json, var_weight):

    statistics = {}
    
    # weight variable is just one variable
   
    if elem["type"] == "cat":
        cat_dict = uni_cat(elem, file_csv, var_weight)

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

def bi(base, elem, scale, file_csv, file_json, split, weight):
    # split: variable for bi-variate analysis
    # base: variable for bi-variate analysis (every variable except split)
    categories = dict()

    for j, temp in enumerate(file_json["resources"][0]["schema"]["fields"]):
        if temp["name"] in split:
            s = temp["name"]
            bi = dict()
            bi[s] = dict()
            for index, value in enumerate(temp["values"]):
                v = value["value"]
                temp_csv = file_csv.copy()
                for row in temp_csv.iterrows():
                    if temp_csv[s][row[0]] != v:
                        temp_csv.ix[row[0], base] = np.nan
                categories[v] = uni(elem, scale, temp_csv, file_json, weight)
                categories[v]["label"] = temp["values"][index]["label"]

                if elem["type"] == "cat":
                    uni_source = uni(elem, scale, file_csv, file_json, weight)
                    for i in ["values", "missings", "labels"]:
                        bi[s][i] = uni_source[i]
                        del categories[v][i]

                elif elem["type"] == "number":
                    uni_source = uni(elem, scale, file_csv, file_json, weight)
                    for i in ["min", "max", "by"]:
                        bi[s][i] = uni_source[i]
                        del categories[v][i]

            bi[s].update(dict(
                label = temp["label"],
                categories = categories,
                ))    

    return bi


def stat_dict(dataset_name, elem, file_csv, file_json, split, weight):
    scale = elem["type"][0:3]

    stat_dict = dict(
        study = "testsuite",
        dataset = dataset_name,
        variable = elem["name"],
        label = elem["label"],
        scale = scale,
        uni = uni(elem, scale, file_csv, file_json, weight),
        )
    if elem["name"] not in split and split!="":
        stat_dict["bi"] = bi(elem["name"], elem, scale, file_csv, file_json, split, weight)

    return stat_dict

def generate_stat(dataset_name, d, m, vistest, split, weight):
    stat = []
    for i, elem in enumerate(m["resources"][0]["schema"]["fields"]):
        temp = d.copy()
        stat.append(
            stat_dict(dataset_name, elem, temp, m, split, weight)
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
    
def write_stats(data, metadata, filename, file_type="json", split="", weight="", vistest=""):
    dataset_name = re.search('^.*\/([^-]*)\..*$', filename).group(1)
    stat = generate_stat(dataset_name, data, metadata, vistest, split, weight)
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
