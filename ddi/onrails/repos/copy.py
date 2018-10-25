"""
This module contains functions to copy files from the ``metadata/`` directory
to the ``ddionrails/`` directory without modification.
"""

import os
import pandas as pd

def f(filename, target=None):
    """
    Copy a file from the ``metadata/`` directory to the ``ddionrails/``
    directory without any modification. Example::

        from ddi.onraily import copy
        copy.f("concepts.csv")


    The option ``target`` allows to rename the file in the process.
    """
    if not target:
        target = filename
    os.system("cp metadata/%s ddionrails/%s" % (filename, target))

def study():
    """
    DEPRECATED

    Copy the file ``study.md`` from the ``metadata/`` directory to the
    ``ddionrails/`` directory without any modification.

    This funciton is deprecated, please use::
    
        from ddi.onrails import copy
        copy.f("study.md")
    """
    os.system("cp metadata/study.md ddionrails")

def bibtex(input_format="latin1"):
    """
    DEPRECATED

    The input format for publications will change soon.
    """
    if input_format == "utf8":
        os.system("cp metadata/bibtex.bib ddionrails")
    elif input_format == "latin1":
        os.system("cp metadata/bibtex.bib ddionrails")
        #os.system("recode l1..utf8 ddionrails/bibtex.bib")
    else:
        raise Exception("Invalid input_format")

def r2ddi(in_path, out_path):
    """
    DEPRECATED

    The DDI-based XML is no longer part of the import formats for DDI on Rails.
    """
    os.system("""
        rm -r ddionrails/r2ddi
        mkdir -p ddionrails/r2ddi/
        cp -r %s %s
    """ % (in_path, out_path))
