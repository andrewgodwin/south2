#!/usr/bin/env python

import os
from setuptools import setup, find_packages

os.environ['SOUTH_NO_MONKEY_PATCH'] = "1"
from south import __version__

setup(
    name='South',
    version=__version__,
    description='South: Migrations for Django',
    long_description='South 2 is a database migrations library for the Django web framework, implementing Django\'s native migrations from 1.7 for 1.4 - 1.6.',
    author='Andrew Godwin',
    author_email='andrew@aeracode.org',
    url='http://south.aeracode.org/',
    download_url='http://south.aeracode.org/wiki/Download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(),
)
