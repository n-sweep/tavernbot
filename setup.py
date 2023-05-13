#!/usr/bin/env python

from setuptools import setup

setup(
    name='tavernbot',
    version='0.01',
    description='gotbot',
    author='n_sweep',
    author_email='n@sweep.sh',
    packages=['tavernbot'],
    install_requires=[  # external package dependencies
        'discord',
    ]
)
