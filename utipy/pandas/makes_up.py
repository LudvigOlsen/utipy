#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

# Import operator module for dynamically passing operators
from typing import Union
from numbers import Number
import pandas as pd
import operator
import numpy as np
from utipy.utils.convert_to_type import convert_to_type


def makes_up(
    x: Union[pd.Series, np.ndarray, list],
    value: Union[str, Number],
    thresh: float,
    direction: str = '>',
    missing_error: bool = False
):
    """
    Checks the percent-wise appearance of a specific value (or any value) in a Series
    against a threshold and a given direction.

    Asks:
        'Does [value] make up [direction] than [thresh] percent of `x`?'
    E.g.:
        'Does 0 make up more than 90 percent of `x`?'


    Parameters
    ----------
    x : pd.Series, np.ndarray, list
        The values to check. Array-like objects will be converted to pd.Series internally.
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
        Raise error if value is not in `x`.


    Returns
    -------
    bool


    Examples
    --------
    
    Does '0' make up less than 30% of `x`?
    >>>  makes_up(
    ...     x, 
    ...     value = '0', 
    ...     thresh = 0.3, 
    ...     direction = '<'
    ... )

    Any NaNs in `x`? 

    >>> makes_up(
    ...     x, 
    ...     value = 'NaN', 
    ...     thresh = 0, 
    ...     direction = '>'
    ... )

    Does `x` only contain 1 unique value?
    I.e. the same value in 100% of the rows.
    >>>  makes_up(
    ...     x, 
    ...     value = 'any',
    ...     thresh = 1, 
    ...     direction = '=='
    ...  )

    """

    # Make sure directioon is given as '>', '<', '<=', '>=', or '=='
    if not direction in ['>', '<', '<=', '>=', '==']:
        raise ValueError(
            '`direction` can only be given as \'>\',\'<\',\'>=\',\'<=\', or \'==\'.')

    # Create dictionary for calling operator
    # Uses module: operator
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '==': operator.eq}

    # Make sure thresh is given as a number between 0 and 1
    if not (thresh >= 0 and thresh <= 1):
        raise ValueError(
            '`thresh` had an incorrect format. '
            'Pass as a percentage (between 0-1).')

    # Check if x is a pd.Series
    # and convert if necessary
    x = convert_to_type(x, 'pd.Series')

    # If it is an object, we can only recognize NaN and inf as strings
    # and fall back to checking it as a string
    if x.dtype in [np.dtype('object')] and value in ['NaN', 'inf', 'any']:
        # When converted to string,
        # np.nan becomes 'nan'
        if value == 'NaN':
            value = 'nan'

        # Make sure that object elements are considered strings
        x = x.apply(str)

        # First check if value is 'any'
        if value == 'any':
            n_value = x.value_counts(dropna=False).max()

        # First we check if value is in x at all
        elif not (value in set(x)):
            # If asked to raise error if value is not found
            # raise error
            if missing_error:
                raise ValueError('`value` not found in `x`')
            # Else, it was found 0 times in series
            else:
                n_value = 0
        else:
            # If it IS in `x``,
            # count how many times
            n_value = x.value_counts(dropna=False)[value]

    elif value == 'NaN':
        n_value = x.isnull().sum()

    elif value == 'inf':
        try:
            n_value = np.isinf(x).sum()
        except:
            raise ValueError(
                "`value` ('inf') could not be searched for in `x`.")

    elif value == 'any':
        n_value = x.value_counts(dropna=False).max()

        # If n_value is NaN we want to convert it
        # to a number instead. So the number of
        # NaNs.
        if np.isnan(n_value):
            n_value = x.isnull().sum()

    # Check if value is not in `x`
    elif value not in set(x):
        # If asked to raise error if value is not found
        if missing_error:
            raise ValueError('value not found in `x`')
        # Else, it was found 0 times in series
        else:
            n_value = 0
    # If value in `x``
    else:
        # Get how many times value is in col
        n_value = x.value_counts()[value]

    # Get total number of values in col
    total_values = len(x)

    # Check with the given direction (operator) if n_value
    # exceeds the threshold
    return ops[direction]((n_value / float(total_values)), thresh)
