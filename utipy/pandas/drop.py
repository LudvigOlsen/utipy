#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:24:02 2017

@author: ludvigolsen
"""

#import pandas as pd
#import numpy as np
import logging
from .makes_up import makes_up

def drop(df, 
         value = 'NaN',
         thresh = 0,
         direction = '>',
         axis = 0,
         cols = None,
         verbose = False):
    
    """
    Drop rows or columns from pandas DataFrame based on values.
    Find if specific values, or any values, are represented too much, too little, etc.
    
    
    ---
    
    Arguments:
    
    df : pd.DataFrame
    value : value to match
        allowed values:
            regular value,
            'any',
            'NaN',
            'inf'
    thresh : threshold in percentage (0-1)
    direction -  '>', '<', '>=', '<=', or '=='
        defaults to '>' meaning 'more than [thresh] percent *bad* values' 
    axis : 0 for columns, 1 for rows
    cols : array of column names for searching within
    
    ---
    
    Example:
    
    # Remove all rows with any NaNs in dependent variable 'y'
    drop(df, value = 'NaN', axis = 1, thresh = 0, 
         direction = '>', cols = ['y'])
         
    # Remove all columns with only 1 unique value.
    # I.e. the same value in 100% of the rows.
    drop(df, value = 'any', axis = 0, thresh = 1, 
         direction = '==')
    
    # Remove all columns that have less than 30% NaNs
    drop(df, value = 'NaN', axis = 0, thresh = 0.3, direction = '<')
    
    """

    if verbose:
        # Get logger
        logging.getLogger(__name__).addHandler(logging.NullHandler())
    
    if value is None:
        
        if verbose:
            
            logging.error('ValueError: value cannot be None.')
            
        raise ValueError('value cannot be None.')
    
    # Create copy of dataframe
    data = df.copy()
    
    if cols is not None:

        # Subset dataframe to only work on cols
        data_cols = data.filter(items=cols)

        # Find columns / rows to drop
        to_drop = _find_exceeders(data_cols, value, 
                                 thresh, direction,
                                 axis = axis, 
                                 verbose = verbose)

    else:

        # Find columns / rows to drop
        to_drop = _find_exceeders(data, value, thresh, 
                                 direction, axis = axis, 
                                 verbose = verbose)

    # Drop columns / rows

    if axis == 0:

        if verbose:

            logging.info('Dropped {} columns'.format(len(to_drop)))
            
        return(data.drop(to_drop,axis=1))
 
    elif axis == 1: 

        if verbose:

            logging.info('Dropped {} rows'.format(len(to_drop)))
        
        return(data.drop(data.index[to_drop], axis=0))

    else:

        if verbose:
            
            logging.error('ValueError: value cannot be None.')
            
        raise ValueError("axis must be 0 or 1")
            
            
            
# Wrapper for calling exceede_tresh - for finding columns / rows to drop
def _find_exceeders(data, value, thresh, direction, axis, verbose = False):

    if verbose:
        logging.getLogger(__name__)
    
    exceeders = data.apply(makes_up, axis = axis, value=value, 
               thresh=thresh, direction=direction)

    if axis == 0:

        # Find columns to drop
        to_drop = [col for col,exceedes in zip(data.columns,exceeders) if exceedes]

    elif axis == 1:

        # Find rows to drop
        to_drop = [row for row, exceedes in zip(data.index, exceeders) if exceedes]

    else: 

        if verbose:
            
            logging.error('ValueError: axis must be 0 or 1.')
            
        raise ValueError("axis must be 0 or 1.")

    return(to_drop)
        


    

    



