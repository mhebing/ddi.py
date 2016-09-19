import glob, re
from collections import defaultdict
from lxml import etree

D_RE = re.compile(r'r2ddi/([\w\d]+)/([\w\d]+)/([\w\d]+\.xml)')

def parse_dataset(dataset):
    pass

def parse_all_datasets(version, language)
    structure = defaultdict(lambda: defaultdict(dict))
    for filename in glob.glob("r2ddi/*/*/*xml"):
        x = D_RE.findall(filename)[0]
        structure[x[0]][x[1]][x[2]] = filename

def main(version="v1", language="en"):
    parse_all_datasets(version, language)
