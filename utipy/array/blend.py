#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:16:39 2017

@author: ludvigolsen
"""

import numpy as np

def blend(x1, x2, amount = 0.5):
    
    x1_weighted = np.multiply(x1, (1 - amount))
    x2_weighted = np.multiply(x2, amount)
    
    return(x1_weighted + x2_weighted)