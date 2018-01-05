from jinja2 import Template
import os, sys
import re
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

template_do = """
clear
set more off
capture log close
import delimited ../input/{{ data_name }}, varnames(1) clear
/*
drop v1
*/

{% for x in input_list %}
label variable {{ x["name"].lower() }} "{{ x["label"] }}"
{% if x["type"] == "cat" %}
{% for y in x["values"] %}
label define {{ x["name"].lower() }}_label {{ y["value"] }} "{{ y["label"] }}", add
{% endfor %}
label values {{ x["name"].lower() }} {{ x["name"].lower() }}_label
{% endif %}
{% endfor %}
"""

def save_do(output_do, do):

    logger.info("write \"" + output_do + "\"")
    with open(os.path.join(output_do), "w") as field1:
        field1.write(do)

def generate_do(data_name, file_csv, file_json):
    template = Template(template_do)
    meta = template.render(
        input_list=file_json["resources"][0]["schema"]["fields"],
        data_name=data_name,
    )
    return meta
    
def write_stata(d, m, output_do):
    data_name = re.sub(".do", ".csv", re.search('^.*\/(.*)', output_do).group(1))
    do = generate_do(data_name, d, m)
    save_do(output_do, do)
