write_stats.py
==============

Parameters:
-----------

.. csv-table::
   :widths: 15 40 20
   :header: "Parameter", "Description", "Default"
   :file: parameter_write_stats.csv

.. function:: uni_cat(elem, elem_de, file_csv, var_weight)

    get frequencies, values, missings, labels and weighted values

.. function:: uni_string(elem, file_csv)

    count frequencies of identical values and missings

.. function:: uni_number(elem, file_csv, var_weight, num_density_elements=20)

    get frequencies, labels and values from numerical variables
    
    calculate density and min/max

.. function:: stats_cat(elem, file_csv)

    get ordinal statistics from categorical variables i.e. median

.. function:: stats_number(elem, file_csv)

    get numerical statistics from numerical variables i.e. mean and median

.. function:: stats_string(elem, file_csv)

    get valid, invalid and total values from string variables

.. function:: uni_statistics(elem, file_csv)

    look for variable type (category, string or number) and pass it to **uni_cat**, **uni_string** or **uni_number**

.. function:: uni(elem, elem_de, file_csv, var_weight)

    look for variable type (category, string or number) and pass it to **uni_cat**, **uni_string** or **uni_number**

.. function:: bi(base, elem, elem_de, scale, file_csv, file_json, split, weight)

    creates bivariate statistics for given variables

    temp contains meta information to each variable
    
    filter variables for each value of the split variable
    
    pass filtered variables to **uni**
    
    i.e. get filtered statistics of income by gender

.. function:: stat_dict(dataset_name, elem, elem_de, file_csv, file_json, file_de_json, split, weight, analysis_unit, period, sub_type, study, log)

    prepare a dict for statistics
    
    get univariate statistics from **uni**
    
    get bivariate statistics from **bi**
    
    if there are more than 10 cases in dataset:
    
        get distribution statistics from **uni_statistics**

.. function:: generate_stat(dataset_name, data, metadata, metadata_de, vistest, split, weight, analysis_unit, period, sub_type, study, log)

    extract variables from metadata
    
    pass every variable individually to **stat_dict**
    
    calls **write_vistest**

.. function:: write_vistest(stat, dataset_name, var_name, vistest)

    generate a testfile for the visualization

.. function:: write_stats(data, metadata, filename, file_type="json", split="", weight="", analysis_unit="", period="", sub_type="", study="", metadata_de="", vistest="", log= "")

    first script to be executed
    
    gets statistics from **generate_stat**
    
    save statistics as json (default), yaml or html
    
    


