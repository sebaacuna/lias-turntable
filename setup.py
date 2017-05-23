#!/usr/bin/env python
from setuptools import setup, find_packages

project_name = "lias-turntable"

setup(
    name=project_name,
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'python-mpd2',
        'RPi.GPIO',
    ],
    entry_points='''
        [console_scripts]
        turntable=turntable:cli
    '''
)
