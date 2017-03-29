#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:55:12 2017

@author: ludvigolsen
"""

from utipy.groups.methods import l_sizes
from utipy.groups.methods import n_dist

def group(data, n, col = None, method = 'n_dist'):
    """
    Adds a grouping factor
    to dataframe
    
    """
    
    # If no column is given
    # We use the first column in data
    if col is None:
        
        # Get first column of data
        column = data.ix[:,0]
        
        # Create grouping factor
        if method == 'n_dist':
            all_group_ids = n_dist(column, n, randomize = True)
        elif method == 'l_sizes':
            all_group_ids = l_sizes(column, n, randomize = True)
    
    # Else we use the given column
    else:
        
        # Create grouping factor
        if method == 'n_dist':
            all_group_ids = n_dist(data[col], n, randomize = True)
        elif method == 'l_sizes':
            all_group_ids = l_sizes(data[col], n, randomize = True)
    
    # Add grouping factor to data
    data['group'] = all_group_ids
    
    return(data)