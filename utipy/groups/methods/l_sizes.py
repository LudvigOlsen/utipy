#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np
from random import shuffle

def _l_sizes(v, p, randomize = False, rounding = 'floor'):
    
    """
    Creates grouping factor from group size(s)
    
    p is given as percentage (0-1)
    
    rounding: Floors percentages by default
    Alternative setting: 'round' or 'ceil'
    
    If sum of p is less than 1 an extra group
    with excess elements are appended to the end.
    
    If sum of p is 1 any excess element from
    rounding is added to the last group. I.e.
    given 9 elements and p = [0.5,0.5] l_sizes
    will return 0,0,0,0,1,1,1,1,1.
    """
    
    # If p is passed as scalar
    # Convert to array
    if not hasattr(p, "__iter__"):
    #if not isinstance(p, list):
        p = [p]
        
    # Check if p sums to more than 1
    if not 0 <= sum(p) <= 1:
        raise ValueError('l_sizes: sum of p is not equal to or within 0 and 1')
    
    # Check if the sum of p is 0, 1 or in-between
    if False in [0 <= size <= 1 for size in p]:
        raise ValueError('l_sizes: element of p is not equal to or within 0 and 1')
    
    # Is sum of p 1? Then we only want the number
    # of groups passed.
    if sum(p) == 1:
        fixed_n_groups = True
    else:
        fixed_n_groups = False
    
    if not rounding in ['floor','round','ceil']:
        raise ValueError('l_sizes: rounding must be either floor, round, or ceil')
    
    # Find the sizes based on percentages given
    # Use rounding as specified by user
    if rounding == 'floor':
        sizes = np.floor([len(v)*size for size in p])
    elif rounding == 'round':
        sizes = np.round([len(v)*size for size in p])
    elif rounding == 'ceil':
        sizes = np.ceil([len(v)*size for size in p])
    
    # Find the remaining elements
    excess = len(v) - sum(sizes) 
    
    # If any remaining elements
    if excess >= 0:
        if fixed_n_groups:
            sizes = np.append(sizes[:-1], sizes[-1:]+excess)
        else:
            # Add as size of last groups
            sizes = np.append(sizes, excess) 
    
    # Check that we do not create more values than is in v
    if sum(sizes) != len(v):
        raise ValueError('l_sizes: Wrong number of elements in sizes')
    
    # Create grouping factor
    grouping_factor = np.asarray([[group]*size for size,group in zip(sizes,xrange(len(sizes)))])
    
    # Flatten grouping factor
    grouping_factor = [item for sublist in grouping_factor for item in sublist]
    
    # If randomize is True, shuffle grouping factor
    if randomize:
        shuffle(grouping_factor)
    
    return(grouping_factor)
   