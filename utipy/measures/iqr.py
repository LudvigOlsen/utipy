#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:25:23 2017

@author: ludvigolsen
"""

import numpy as np

## Helpers

def iqr(x):
    
    q75, q25 = np.percentile(x, [75 ,25])
    iqr = q75 - q25
    
    return(iqr)

