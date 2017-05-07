#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np

## Helpers

def _iqr(x):
    
    q75, q25 = np.percentile(x, [75 ,25])
    iqr = q75 - q25
    
    return(iqr)

