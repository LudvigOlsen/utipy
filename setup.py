#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:14:24 2017

@author: ludvigolsen
"""

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='utipy',
      version='0.1.2',
      description='Utility functions for python',
      long_description='Pandas operations. Data grouping, folding, and partitioning.',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='pandas groups folds kfold partitioning utilities tools',
      url='http://github.com/ludvigolsen/utipy',
      author='Ludvig Renbo Olsen',
      author_email='mail@ludvigolsen.dk',
      license='MIT',
      packages=['utipy'],
      install_requires=[
          'pandas',
          'numpy'
      ],
      include_package_data=True,
      zip_safe=False)