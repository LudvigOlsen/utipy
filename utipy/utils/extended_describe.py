#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np
from utipy.measures.iqr import _iqr

# For pandas objects

def _extended_describe(Series):
    
    desc = Series.describe()
    desc['dtype'] = Series.dtype
    desc['median'] = np.median(Series)
    desc['IQR'] = _iqr(Series)
    
    return(desc)
    