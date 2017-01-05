import unittest

def dict_metadata(metadata):
    var_metadata = dict()
    for temp in metadata["resources"][0]["schema"]["fields"]:
        assert "name" in temp, "Name is not in %s" %temp
        assert "label" in temp, "Label is not in %s" %temp
        assert "type" in temp, "Type is not in %s" %temp
        if temp["type"] == "number":
            assert "unique" in temp, "Unique is not in %s" %temp
            if temp["unique"] == 0:
                assert "range" in temp, "Range is not in %s" %temp
        # create var for every entry in fields
        var_metadata["%s" % temp["name"]] = temp
    return var_metadata    

def test_a_unique(dataset, metadata):
    '''
    Test on duplicates in all number variables with unique=1
    '''
    print("Running Unique Vars Check...")
    unique_vars=[]
    detailled={}
    
    var_metadata = dict_metadata(metadata)
    
    for name in var_metadata:
        if(var_metadata[name]["type"]=="number" and var_metadata[name]["unique"]==1):
            unique_vars.append(name)
            dup_lines = []
            for row, bol in dataset[name].duplicated(keep=False).iteritems():
                if bol == True:
                   dup_lines.append(row+2)
            detailled[name] = dup_lines
    not_unique_columns =dataset[unique_vars].columns[dataset[unique_vars].apply(lambda x: len(x) != len(x.unique()), axis=0)]
    assert len(not_unique_columns)==0, "The following variable(s) is/are not unique: %s in lines: %s" % (not_unique_columns, detailled
        )
    print("ok")  


def test_b_uniqueid_notnull(dataset, metadata):
    '''
    Test on missings in the id column.
    '''
    print("Running ID not Null Check...")
    id_col = dataset["id"]
    mis_lines = []
    for row, mis in id_col.isnull().iteritems():
        if mis == True:
            mis_lines.append(row+2)
    assert len(id_col.index[id_col.isnull()]) == 0, "ID column contains Missings in line(s) %s" % mis_lines
    print("ok")        
       
def test_c_validage(dataset, metadata):
    '''
    Test on duplicates in the id column.
    '''
    print("Running Age Check...")
    
    var_metadata = dict_metadata(metadata)    
      
    age_col = dataset["age"] 
    min = var_metadata["age"]["range"][0]
    max = var_metadata["age"]["range"][1]
     
    age_val = []
    age_row = []
    for row, val in age_col.iteritems():
        if val in range(min, max):
            pass
        else:
            age_val.append(val)
            age_row.append(row+2)
                
    assert age_col.between(min, max).all(), "Invalid age(s) %s in line(s) %s" % (age_val, age_row)

    print("ok")
        
def test_d_validsex(dataset, metadata):
    print("Running Sex Check...")
    
    var_metadata = dict_metadata(metadata)    
    
    sex_values = []
    for val in var_metadata["sex"]["values"]:
        sex_values.append(val["value"])
       
    sex_inv_value = []
    sex_inv_row = []
    for row, val in dataset["sex"].iteritems():
        if val in sex_values:
            pass
        else:
            sex_inv_value.append(val)
            sex_inv_row.append(row+2)

    assert len(sex_values) == len(dataset["sex"].unique()), "Undefined value(s) %s in line(s) %s" % (sex_inv_value, sex_inv_row)   
        
    print("ok")
