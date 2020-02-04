import os
from shutil import copy

def f(filename, target=None):
    if not target:
        target = filename
    src = os.path.join("metadata", filename)
    dst = os.path.join("ddionrails", target)
    copy(src, dst)
    print("Copy %s to %s" % (src, dst))


def study():
    f("study.md")

def bibtex(input_format="latin1"):
    if input_format == "utf8":
        os.system("cp metadata/bibtex.bib ddionrails")
    elif input_format == "latin1":
        os.system("cp metadata/bibtex.bib ddionrails")
        # os.system("recode l1..utf8 ddionrails/bibtex.bib")
    else:
        raise Exception("Invalid input_format")


def r2ddi(in_path, out_path):
    os.system(
        """
        rm -r ddionrails/r2ddi
        mkdir -p ddionrails/r2ddi/
        cp -r %s %s
    """
        % (in_path, out_path)
    )
