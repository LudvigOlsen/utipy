#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np
from random import shuffle

def _n_dist(v, n, randomize = False):
    """
    Creates grouping factor with
    distributed excess elements
    
    """
    len_v = float(len(v))
    
    divisor = len_v/n
    
    # Create range the length of v (+1 because it starts at 0)
    # Divide each element and get everything but the first element (0)
    v_divided = [vi / divisor for vi in xrange(int(len_v)+1)][1:]
    
    # First round to a smaller decimal number to avoid ceil of
    # e.g. 7.00000000...03 becoming 8
    # Then round up to nearest integer
    v_ceiled = np.ceil(np.around(v_divided, 5)).astype(int)
    
    if randomize:
        
        shuffle(v_ceiled)
    
    return(v_ceiled)
  