import os
import pandas as pd

def study():
    os.system("cp metadata/study.md ddionrails")

def bibtex():
    os.system("cp metadata/bibtex.bib ddionrails")

def r2ddi(in_path, out_path):
    os.system("""
        rm -r ddionrails/r2ddi
        mkdir -p ddionrails/r2ddi/
        cp -r %s %s
    """ % (in_path, out_path))
