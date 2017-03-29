#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:25:23 2017

@author: ludvigolsen
"""

# Import operator module for dynamically passing operators
import operator
#import pandas as pd
import numpy as np
import logging

def makes_up(Series, value, thresh, direction = '>', missing_error = False, verbose = False):

    """
    Checks if value (or any value) appears in pandas Series more than,
    less than or equal to a threshhold given as percentage.

    To do:
     - Come up with a better name.

    direction -  '>', '<', '>=', '<=', or '=='
        defaults to '>' meaning 'more than [thresh] percent values' 
    thresh : given as percentage (between 0-1)
    value : value to match. 
        To find 'NaN's, pass 'NaN
        To find 'inf's, pass 'inf'
        'Any

    """
    
    logging.getLogger(__name__)
    
    # Make sure directioon is given as '>', '<', '<=', '>=', or '=='
    if not (direction in ['>','<','<=', '>=', '==']):
        
        if verbose:
            
            logging.error('ValueError: direction can only be given as \'>\',\'<\',\'>=\',\'<=\', or \'==\'')
        
        raise ValueError('direction can only be given as \'>\',\'<\',\'>=\',\'<=\', or \'==\'')
 
    # Create dictionary for calling operator
    # Uses module: operator
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq}
    
    # Make sure thresh is given as a number between 0 and 1
    if not (thresh >= 0 and thresh <= 1):
        
        if verbose:
            
            logging.error('ValueError: threshold incorrect format. Give as percentage (between 0-1)')
        
        raise ValueError('threshold incorrect format. Give as percentage (between 0-1)')

    if value == 'NaN':
        n_value = Series.isnull().sum()
        
    elif value == 'inf':
        n_value = np.isinf(Series).sum()
    
    elif value == 'any':
        n_value = Series.value_counts().max()
            
        # If n_value is NaN we want to convert it
        # to a number instead. So the number of 
        # NaNs.
        if np.isnan(n_value):
            n_value = Series.isnull().sum()
    
    # Check if value is not in Series
    elif not (value in set(Series)):
        
        # If asked to raise error if value is not found
        # raise error
        if missing_error:
            
            if verbose:
            
                logging.error('ValueError: value not found in Series')
            
            raise ValueError('value not found in Series')
        
        # Else, set it was found 0 times in series
        else:
            n_value = 0
    
    # If value in Series 
    else:
        
        # Get how many times value is in col
        n_value = Series.value_counts()[value]
        
    # Get total number of values in col
    total_values = len(Series)
    
    # Check with the given direction (operator) if n_value
    # exceeds the threshold
    if ops[direction]((n_value / float(total_values)), thresh):
        return(True)
    else:
        return(False)