#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import pandas as pd
from utipy.pandas import subset_by_levels
from .group_uniques import group_uniques
from .group import group

def fold(data, n=5, id_col=None, cat_col=None, 
         return_factor = False):
    """
    Creates balanced folds.
    Balance on a categorical column
    and/or make sure that datapoints that share 
    an ID (e.g. participant id) are kept in the
    same folds.
    
    """
    
    # Make data a copy of data
    # As the sorting index elsewise
    # seem to be added to the given dataframe
    # in the outer environment/function
    data = data.copy()
    
    # Create temporary index that we will
    # use to reorder the dataframe later
    data['.sorting_index'] = range(len(data))
    
    # If user specified id_col
    if id_col is not None:
        
        # And if user specified cat_col
        if cat_col is not None:

            # Subset data by levels of categorical column
            cat_subsets = subset_by_levels(data, cat_col)

            # Create groups for each subset based on unique values in id_col
            # Concatenate subsets with the new grouping factor
            data = pd.concat([group_uniques(data, n, id_col) for data in cat_subsets])
    
        else: 
            
            # Create groups based on unique values in id_col
            data = group_uniques(data, n, id_col)
     
    else:
        
        # If user specified cat_col (but not id_col)
        if cat_col is not None:
            
            # Subset data by levels of categorical column
            cat_subsets = subset_by_levels(data, cat_col)
            
            # Group each subset and concatenate subsets
            data = pd.concat([group(data, n, cat_col) for data in cat_subsets])
            
        # If neither id_col or cat_col is specified
        else:
            
            # Group data by the first column in data
            # group() does this automatically if not 
            # given a column.
            data = group(data, n)
            
    # Sort data by the sorting index 
    # and remove the sorting index
    data = data.sort_values('.sorting_index').drop('.sorting_index', 1)
    
    # If return factor is True
    if return_factor:
        
        # Only the return the grouping factor
        return(data['group'])
    
    else:
        
        # Return data
        return(data)
