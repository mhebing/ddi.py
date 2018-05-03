write_stata.py
==============

Parameters
----------
+----------------+---------------------------+
| Parameter      | Description               |
+================+===========================+
| d              | Dataset                   |
|                |                           |
| m              | Metadata                  |
|                |                           |
| output_do      | Location for the Do file  |
+----------------+---------------------------+

Functions
---------

.. function:: save_do(output_do, do)

    save do as do file in output_do (path)

.. function:: generate_do(data_name, file_csv, file_json)

    generate do file with :ref:`template`
    return the final do file structure

.. function:: write_stata(d, m, output_do)

    call generate_do and save_do
    
.. _template:

Template
--------

.. code-block:: do

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

