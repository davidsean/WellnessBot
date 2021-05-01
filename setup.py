#!/usr/bin/python3
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# meta-data.
NAME = 'Wellness Bot'
DESCRIPTION = 'Activity bot for discord servers'
EMAIL = 'david.sean@gmail.com'
AUTHOR = 'David Sean, Paul Laplante, Christian Sargusingh'
REQUIRES_PYTHON = '>=3.8.0'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt'), 'r') as requirements:
    REQUIRED = list()
    for line in requirements.readlines():
        REQUIRED.append(line)

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
project_slug = "app"
with open(os.path.join(here, project_slug, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url='https://github.com/davidsean/WellnessBot',
    download_url='',
    python_requires=REQUIRES_PYTHON,
    scripts=[
        'bin/start'
    ],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=REQUIRED,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Office/Business :: Scheduling'
    ],
)
