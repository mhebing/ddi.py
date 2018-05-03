write_stats.py
==============

Parameters:
-----------

data
++++

    dataset

metadata
++++++++

    metadata

filename
++++++++

    Name of the output file

file_type (optional)
+++++++++

    save stats as json, yaml or html
    
    default is json

split (optional)
+++++

    contains variable(s) for bivariate statistics
    
    default is empty

weight (optional)
++++++

    contains weight variable
    
    dafault is empty

analysis_unit (optional)
+++++++++++++



period (optional)
++++++



sub_type (optional)
++++++++



study (optional)
+++++



metadata_de (optional)
+++++++++++



vistest (optional)

    contains path for a vistest file
    
    no vistest if remained empty
    
    default is empty

log (optional)

    contains path for a log file
    
    no log if remained empty
    
    daufault is empty

.. function:: uni_cat(elem, elem_de, file_csv, var_weight)

.. function:: uni_string(elem, file_csv)

.. function:: uni_number(elem, file_csv, var_weight, num_density_elements=20)

.. function:: stats_cat(elem, file_csv)

.. function:: stats_number(elem, file_csv)

.. function:: stats_string(elem, file_csv)

.. function:: uni_statistics(elem, file_csv)

.. function:: uni(elem, elem_de, file_csv, var_weight)

.. function:: bi(base, elem, elem_de, scale, file_csv, file_json, split, weight)

.. function:: stat_dict(dataset_name, elem, elem_de, file_csv, file_json, file_de_json, split, weight, analysis_unit, period, sub_type, study, log)

.. function:: generate_stat(dataset_name, data, metadata, metadata_de, vistest, split, weight, analysis_unit, period, sub_type, study, log)

.. function:: write_vistest(stat, dataset_name, var_name, vistest)

.. function:: write_stats(data, metadata, filename, file_type="json", split="", weight="", analysis_unit="", period="", sub_type="", study="", metadata_de="", vistest="", log= "")

    first script to be executed
    
    call **generate_stat**


