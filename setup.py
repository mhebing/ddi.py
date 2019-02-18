#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Template used:
# https://github.com/kennethreitz/setup.py

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "ddi"
DESCRIPTION = "DDI related tools"
URL = "https://github.com/ddionrails/ddi.py"
EMAIL = "marcel@ddionrails.org"
AUTHOR = "Marcel Hebing"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.0"

# What packages are required for this module to be executed?
REQUIRED = ["jinja2", "lxml", "pandas", "pyyaml", "scipy"]

# What packages are optional?
EXTRAS = {}


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
)
