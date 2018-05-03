dataset.py
==========

.. class:: Dataset

    Dataset allows the user to read, test and export data in different formats.
    
    Example:
        dataset = Dataset()
        dataset.read_stata("../input/dataset.dta")
        dataset.test()
        dataset.write_stats("../output/dataset.json")
        dataset.write_tdp("../output/dataset.csv", "../output/dataset.json")
        
.. function:: read_tdp(self, csv_name, json_name)

    Function to read data in tabular data package format.
        
    Parameter:
        csv_name: Name of the row data in tabular format
        json_name: Name of the metadata in json format
        
    Example:
        dataset.read_tdp("../input/dataset.csv", "../input/dataset.json")
        
.. function:: read_stata(self, dta_name)
    
    Function to read data in stata format.
        
    Parameter:    
        dta_name: Name of the data in stata format
        
    Example:   
        dataset.read_stata("../input/dataset.dta") 

.. function:: write_stats(self, output_name, file_type="json", split="", weight="", analysis_unit="", period="", sub_type="", study="", metadata_de="", log="")

    Function to write statistics from data in json/html format.
        
    Parameter:    
        output_name: Name of the output file
        file_type: Statistics are read out in json or html; Standard is "json"
        split: Name of the variable(s) for bivariate statistics; Standard is ""
        weight: Name of the weight variable; Standard is ""
        
    Example:    
        dataset.write_stats("../output/dataset.html", file_type="html", split="split", weight="weight") 

.. function:: write_tdp(self, output_csv, output_json)

    Function to write data in tdp format.
        
    Parameter:    
        output_csv: Name of the row data in tabular format
        output_json: Name of the metadata in json format
        
    Example:    
        dataset.write_tdp("../output/dataset.csv", "../output/dataset.json") 

.. function:: write_stata(self, output_name)

    Function to write data in stata format.
        
    Parameter:    
        output_name: Name of the data in stata format
        
    Example:    
        dataset.write_stata("../output/dataset.dta")

.. function:: test(self)

    Function to test data:
        completeness of the metadata
        correctness of unique values (i.e. id)
        correctness of range (i.e. age)
        Checking if the number of values of categorical variables in the data is equal to the number in the metadata
        
    Parameter:
        
        none
        
    Example:
        
        dataset.test()
