#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import logging
from .makes_up import makes_up

def drop(data, 
         value = 'NaN',
         thresh = 0,
         direction = '>',
         axis = 0,
         cols = None,
         verbose = False):

    """Drop rows or columns from pandas DataFrame based on values.

    Drop rows / columns if specific value, or any value, is represented too much, too little, etc.
    
    Commands:
        'Drop [axis] if [value] appears [direction] than [thresh] percent of the time.'
    E.g.:
        'Drop columns if 0 appears more than 90 percent of the time.'
        'Drop rows if *any* value appears exactly 77 percent of the time.'


    Parameters
    ----------
    data : pd.DataFrame
        The data to distort.
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
    axis : int
        0 for columns, 1 for rows.
    cols : list of strings
        Column names to search within.
    verbose : bool
        Log number of dropped rows / columns


    Returns
    -------
    pd.DataFrame


    Examples
    --------
    
    Uncomment code to run.
    
    Remove all rows with any NaNs in dependent variable 'y'
    # drop(data, value = 'NaN', axis = 1, thresh = 0, 
    #      direction = '>', cols = ['y'])
         
    Remove all columns with only 1 unique value.
    I.e. the same value in 100% of the rows.
    # drop(data, value = 'any', axis = 0, thresh = 1, 
    #      direction = '==')
    
    Remove all columns that have less than 30% NaNs
    # drop(data, value = 'NaN', axis = 0, thresh = 0.3, 
    #      direction = '<')

    """
    

    if verbose:
        # Get logger
        logging.getLogger(__name__).addHandler(logging.NullHandler())
    
    if value is None:
        
        if verbose:
            
            logging.error('ValueError: value cannot be None.')
            
        raise ValueError('value cannot be None.')
    
    # Create copy of dataframe
    data = data.copy()
    
    if cols is not None:

        # Subset dataframe to only work on cols
        data_cols = data.filter(items=cols)

        # Find columns / rows to drop
        to_drop = _find_exceeders(data_cols, value, 
                                 thresh, direction,
                                 axis = axis)

    else:

        # Find columns / rows to drop
        to_drop = _find_exceeders(data, value, thresh, 
                                 direction, axis = axis)

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
            
            
            
# Wrapper for calling makes_up - for finding columns / rows to drop
def _find_exceeders(data, value, thresh, direction, axis):
    """Internal wrapper function for calling makes_up()"""

    
    exceeders = data.apply(makes_up, axis = axis, value=value, 
               thresh=thresh, direction=direction)

    if axis == 0:

        # Find columns to drop
        to_drop = [col for col, exceedes in zip(data.columns,exceeders) if exceedes]

    elif axis == 1:

        # Find rows to drop
        to_drop = [row for row, exceedes in zip(data.index, exceeders) if exceedes]

    else: 
            
        raise ValueError("axis must be 0 or 1.")

    return(to_drop)
        


    

    



