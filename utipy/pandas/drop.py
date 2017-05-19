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
         include = None,
         exclude = None,
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
    include : list of strings
        Names of columns / indices of rows to search within. 
        None means ALL are included unless otherwise specified, see *exclude*.
    exclude : list of strings
        Names of columns / indices of rows NOT to search within.
        None means no columns/rows are excluded unless otherwise specified, see *include*.
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

    if exclude is not None and include is not None:
        raise(ValueError("Either include or exclude must be None."))
    
    
    # Columns

    if axis == 0:

        if exclude is not None:
            # Create include list
            include = [col for col in data.columns if col not in exclude]


        if include is not None:

            # Subset dataframe to only work on included cols
            data_cols = data.filter(items=include)

            # Find columns / rows to drop
            to_drop = _find_exceeders(data_cols, value, 
                                     thresh, direction,
                                     axis = axis)

        else:

            # Find columns / rows to drop
            to_drop = _find_exceeders(data, value, thresh, 
                                     direction, axis = axis)

        # Drop columns
        if verbose:

            logging.info('Dropped {} columns'.format(len(to_drop)))
            
        return(data.drop(to_drop,axis=1))
 

    # Rows

    elif axis == 1: 

        # Find columns / rows to drop
        to_drop = _find_exceeders(data, value, thresh, 
                                 direction, axis = axis)

        # Remove indices not in include or in exclude

        if exclude is not None:
            to_drop = [i for i in to_drop if i not in exclude]
        elif include is not None:
            to_drop = [i for i in to_drop if i in include]

        # Drop rows

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

    # Notice:
    # pd apply() passes the Series as objects, even
    # when it's the columns it's working with!

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
        


    

    



