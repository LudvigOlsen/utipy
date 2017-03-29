#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:51:39 2017

@author: ludvigolsen
"""

import pandas as pd

def subset_by_levels(data, cat_col, drop_cat_col = False):
    """
    Subsets dataframe by each level 
    of a categorical value
    
    """
    
    # Find the unique values (levels) 
    # in the given categorical column
    levels = list(set(data[cat_col]))
    
    # Create subsets for each level
    # Saved as a list of dataframes
    subsets = [pd.DataFrame(data[data[cat_col] == l]) for l in levels]
    
    # Remove cat_col
    if drop_cat_col:
        subsets = [d.drop(cat_col, axis = 1) for d in subsets]
    
    # Return subsets
    return(subsets)