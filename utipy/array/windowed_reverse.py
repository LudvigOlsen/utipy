#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np
from utipy.helpers.check_instance import check_instance
from utipy.helpers.convert_to_type import convert_to_type

def windowed_reverse(x, wsize = 2):
    
    """Reverse / flip windows of array

    Parameters
    ----------
    x : list, np.ndarray, pd.Series
        The array to reverse
    wsize: int
    	Window size

    Returns
    -------
    list, np.ndarray, pd.Series
    	Window reversed array with the type of the original

    Examples
    --------
	x = 1,2,3,4,5,6; wsize = 2 returns 2,1,4,3,6,5
	x = 1,2,3,4,5,6; wsize = 3 returns 3,2,1,6,5,4


    """

    # Get instance type (np.ndarray, list, pd.Series)
    instance_type = check_instance(x)
    
    # Window and reverse
    reversed_windows = [x[pos:pos+wsize][::-1] for pos in range(len(x))[::wsize]]
    
    # Flatten windows
    flattened_array = np.concatenate(reversed_windows)
    
    # Convert to original type (np.ndarray, list, pd.Series)
    return(convert_to_type(flattened_array, instance_type))
    