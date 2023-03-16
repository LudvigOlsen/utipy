"""
@author: ludvigolsen
"""

from setuptools import setup, find_packages

with open("utipy/about.py") as f:
    v = f.read()
    for l in v.split("\n"):
        if l.startswith("__version__"):
            __version__ = l.split('"')[-2]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(name='utipy',
      version=__version__,
      description='Utility functions for python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Utilities',
      ],
      keywords='pandas numpy array ndarray groups folds kfold partitioning utilities tools rolling windows time',
      url='http://github.com/ludvigolsen/utipy',
      author='Ludvig Renbo Olsen',
      author_email='mail@ludvigolsen.dk',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pandas',
          'numpy'
      ],
      include_package_data=True,
      zip_safe=False)
