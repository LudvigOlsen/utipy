#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

from utipy.groups.methods.l_sizes import _l_sizes
from utipy.groups.methods.n_dist import _n_dist

def group(data, n, col = None, method = 'n_dist'):
    """
    Adds a grouping factor
    to dataframe
    
    """
    
    data = data.copy()

    # If no column is given
    # We use the first column in data
    if col is None:
        
        # Get first column of data
        column = data.ix[:,0]
        
        # Create grouping factor
        if method == 'n_dist':
            all_group_ids = _n_dist(column, n, randomize = True)
        elif method == 'l_sizes':
            all_group_ids = _l_sizes(column, n, randomize = True)
    
    # Else we use the given column
    else:
        
        # Create grouping factor
        if method == 'n_dist':
            all_group_ids = _n_dist(data[col], n, randomize = True)
        elif method == 'l_sizes':
            all_group_ids = _l_sizes(data[col], n, randomize = True)
    
    # Add grouping factor to data
    data['group'] = all_group_ids
    
    return(data)