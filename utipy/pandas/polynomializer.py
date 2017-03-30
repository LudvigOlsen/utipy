#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:55:12 2017

@author: ludvigolsen
"""

import pandas as pd
import numpy as np

def polynomializer(data, degree = 2, suffix = '_poly', exclude = None):
    
    """
    Creates polymonial features
    Adds suffix with information on which
    degree a column represents
    

    """
    
    # Create copy of data
    data = data.copy()
    
    if exclude is not None:

        cols_include = [c for c in data.columns if c not in exclude]
        data_include =  data.filter(items = cols_include)
    
    else:

        data_include = data

    # Create dataframes with exponential columns
    polynomialized = [data_include ** deg for deg in range(degree+1)[1:]]
    
    # Function for adding suffix to column names
    def suffixicate(df, deg):
        if deg != 0:
            return(df.add_suffix("{}{}".format(suffix, deg+1)))
        else:
            return(df)
    
    # Add suffices to dataframes
    polynomialized = map(lambda df, deg: suffixicate(df,deg), 
                         polynomialized, range(degree))
    
    # Combine dataframes
    polynomialized = pd.concat(polynomialized, axis = 1)    

    # Combine processed data with excluded data
    data_all = pd.concat([data.filter(items = exclude), polynomialized], axis = 1)

    ## Reorder 

    # First get all the new column names
    new_cols = [c for c in polynomialized.columns if c not in data.columns]

    # Append old and new column names
    all_columns_sorted = np.append(data.columns, new_cols)

    # Reorder dataframe
    data_ordered = data_all.filter(items = all_columns_sorted)

    
    return(data_ordered)
    