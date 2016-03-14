import sys
import os
from paver.easy import *

def run(script):
    for line in script.strip().split("\n"):
        print("\n[SYSTEM] %s" % line.strip())
    os.system(script)

@task
def test():
    run("python -m unittest discover")
