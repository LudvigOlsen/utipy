#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:55:12 2017

@author: ludvigolsen
"""

import pandas as pd

def polynomializer(data, degree = 2, suffix = '_poly'):
    
    """
    Creates polymonial features
    Adds suffix with information on which
    degree a column represents
    
    ### Add Exclude to exclude non-numeric
    

    """
    
    # Create copy of data
    data = data.copy()
    
    # Create dataframes with exponential columns
    polynomialized = [data ** deg for deg in range(degree+1)[1:]]
    
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
    
    return(polynomialized)
    