from jinja2 import Template
import os, sys
import re
import pandas as pd
import numpy as np

def save_do(output_do, do):

    print("write \"" + output_do + "\"")
    with open(os.path.join(output_do), "w") as field1:
        field1.write(do)

def generate_do(data_name, file_csv, file_json):
    with open("script/template.do", "r") as f:
        template = Template(f.read())
    meta = template.render(
        input_list=file_json["resources"][0]["schema"]["fields"],
        data_name=data_name,
    )
    return meta
    
def write_stata(d, m, output_do):
    data_name = re.sub(".do", ".csv", re.search('^.*\/(.*)', output_do).group(1))
    do = generate_do(data_name, d, m)
    save_do(output_do, do)
