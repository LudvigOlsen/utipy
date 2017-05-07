#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import pandas as pd

def subset_by_levels(data, cat_col, drop_cat_col = False):

    """Subsets dataframe by each level of a categorical column
    

    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to subset.
    cat_col : str, int
        Name or index of categorical column to subset by.
    drop_cat_col: bool
        Remove the categorical column from each subset.
    

    Returns
    -------
    list of pd.DataFrames


    Examples
    --------
    
    Uncomment code to run.
    
    # df = pd.DataFrame({'a': [1,2,3,4],
    #                    'b': [2,3,4,5],
    #                    'c': ['a','b','a','b']})
    # subsets = subset_by_levels(df, cat_col = 'c')

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