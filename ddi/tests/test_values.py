def dict_metadata(metadata):
    var_metadata = dict()
    for temp in metadata["resources"][0]["schema"]["fields"]:
        assert "name" in temp, "Name is not in %s" % temp
        assert "label" in temp, "Label is not in %s" % temp
        assert "type" in temp, "Type is not in %s" % temp
        if temp["type"] == "number":
            assert "unique" in temp, "Unique is not in %s" % temp
            if temp["unique"] == 0:
                assert "range" in temp, "Range is not in %s" % temp
        # create var for every entry in fields
        var_metadata["%s" % temp["name"]] = temp
    return var_metadata


def test_unique(dataset, metadata):
    """
    Test on duplicates in all number variables with unique=1
    """
    print("Running Unique Vars Check...")
    unique_vars = []
    detailled = {}

    var_metadata = dict_metadata(metadata)

    for name in var_metadata:
        if var_metadata[name]["type"] == "number" and var_metadata[name]["unique"] == 1:
            unique_vars.append(name)
            dup_lines = []
            for row, bol in dataset[name].duplicated(keep=False).iteritems():
                if bol == True:
                    dup_lines.append(row + 2)
            detailled[name] = dup_lines
    not_unique_columns = dataset[unique_vars].columns[
        dataset[unique_vars].apply(lambda x: len(x) != len(x.unique()), axis=0)
    ]
    assert len(not_unique_columns) == 0, (
        "The following variable(s) is/are not unique: %s in lines: %s"
        % (not_unique_columns, detailled)
    )
    print("ok")


def test_range(dataset, metadata):
    """
    Test on duplicates in the id column.
    """
    print("Running Range Check...")

    var_metadata = dict_metadata(metadata)
    error = []

    for name in var_metadata:
        if var_metadata[name]["type"] == "number" and "range" in var_metadata[name]:
            var_col = dataset[name]
            min = var_metadata[name]["range"][0]
            max = var_metadata[name]["range"][1]

            var_val = []
            var_row = []
            for row, val in var_col.iteritems():
                if val in range(min, max):
                    pass
                else:
                    var_val.append(val)
                    var_row.append(row + 2)

            if len(var_val) > 0:
                error.append(
                    "The variable %s contains value(s) %s out of range in line(s) %s"
                    % (name, var_val, var_row)
                )
    assert len(error) == 0, "%s" % (error)

    print("ok")


def test_values(dataset, metadata):
    print("Running Value Check...")

    var_metadata = dict_metadata(metadata)
    error = []

    for name in var_metadata:
        if var_metadata[name]["type"] == "cat" and "values" in var_metadata[name]:
            values = []
            for val in var_metadata["sex"]["values"]:
                values.append(val["value"])

            inv_value = []
            inv_row = []
            for row, val in dataset["sex"].iteritems():
                if val in values:
                    pass
                else:
                    inv_value.append(val)
                    inv_row.append(row + 2)
            if len(inv_value) > 0:
                error.append(
                    "The variable %s contains undefined value(s) %s in line(s) %s"
                    % (name, inv_value, inv_row)
                )

    assert len(error) == 0, "%s" % (error)

    print("ok")
