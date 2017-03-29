#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:16:39 2017

@author: ludvigolsen
"""

import numpy as np
from pandas_utils.iqr import iqr

# For pandas objects

def _extended_describe(Series):
    
    desc = Series.describe()
    desc['dtype'] = Series.dtype
    desc['median'] = np.median(Series)
    desc['IQR'] = iqr(Series)
    
    return(desc)
    