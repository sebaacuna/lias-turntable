#!/usr/bin/env python
from setuptools import setup, find_packages

project_name = "lias-turntable"

setup(
    name=project_name,
    version='0.1',
    packages=find_packages(),
    scripts=[
        'scripts/turntable'
    ],
    install_requires=[
        'zmq',
        'python-mpd2'
    ]
)
