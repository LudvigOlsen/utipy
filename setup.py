#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='utipy',
      version='0.2.0',
      description='Utility functions for python',
      long_description='Pandas and array operations. Data grouping, folding, and partitioning.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='pandas numpy array ndarray groups folds kfold partitioning utilities tools',
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