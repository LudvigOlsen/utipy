#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

# Import operator module for dynamically passing operators
import operator
import numpy as np
import pandas as pd
from utipy.helpers.convert_to_type import convert_to_type

def makes_up(Series, value, thresh, direction = '>', missing_error = False):
    
    """Checks the percent-wise appearance of a specific value (or any value) in a Series
    against a threshold and a given direction.

    Asks:
        'Does [value] make up [direction] than [thresh] percent of the Series?'
    E.g.:
        'Does 0 make up more than 90 percent of the Series?'


    Parameters
    ----------
    Series : pd.Series, np.ndarray, list
        The Series to check. Array-like objects will be converted to pd.Series internally.
    value : str / int / float
        The value to match.
            Regular value,  
            'any',  
            'NaN',  
            'inf'  
    thresh : float
        Threshold.
        Percentage between 0-1.
    direction : str
        Operator sign for comparison.
            '>', '<', '>=', '<=', '=='.
    missing_error : bool
        Raise error if value is not in Series.


    Returns
    -------
    bool


    Examples
    --------
    
    Uncomment code to run.
    
    Any NaNs in the Series?
    # makes_up(Series, value = 'NaN', thresh = 0, 
    #          direction = '>')
         
    Does the Series only contain 1 unique value?
    I.e. the same value in 100% of the rows.
    # makes_up(Series, value = 'any', thresh = 1, 
    #          direction = '==')
    
    Does '0' make up less than 30% of the Series?
    # makes_up(Series, value = '0', thresh = 0.3, 
    #          direction = '<')

    """
    
    # Make sure directioon is given as '>', '<', '<=', '>=', or '=='
    if not (direction in ['>','<','<=', '>=', '==']):
        
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
        
        raise ValueError('threshold incorrect format. Give as percentage (between 0-1)')

    # Check if Series is a pd.Series
    # and convert if necessary
    Series = convert_to_type(Series, 'pd.Series')

    # If it is an object, we can only recognize NaN and inf as strings
    # and fall back to checking it as a string
    
    if Series.dtype in [pd.np.dtype('object')] and value in ['NaN', 'inf', 'any']:

        # When converted to string,
        # np.nan becomes 'nan'
        if value == 'NaN':
            value = 'nan'

        # Make sure that object elements are considered strings
        Series = Series.apply(str)

        # First check if value is 'any'
        if value == 'any':
            n_value = Series.value_counts().max()

        # First we check if value is in the Series at all
        elif not (value in set(Series)):

            # If asked to raise error if value is not found
            # raise error
            if missing_error:
                
                raise ValueError('value not found in Series')
            
            # Else, it was found 0 times in series
            else:
                n_value = 0
        else:

            # If it IS in the Series,
            # count how many times
            n_value = Series.value_counts()[value]


    elif value == 'NaN':
        n_value = Series.isnull().sum()
        
    elif value == 'inf':

        try:
            n_value = np.isinf(Series).sum()

        except:
            raise(ValueError(
                  "Value 'inf' could not be searched for in Series"))
  
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