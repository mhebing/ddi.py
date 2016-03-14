import pandas as pd
import numpy as np
from lxml.builder import ET
from ddi import ddi, statareader

test1 = statareader.read_stata("test/data/test1.dta")
test1.add_statistics()
