#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np
from utipy.helpers.check_instance import check_instance
from utipy.helpers.convert_to_type import convert_to_type

def window(x, size = 2, gap=1, sample_rate = 1, 
           rolling=True, reverse_direction = False,
           discard_shorts=True):
    """
    
    Splits array, e.g. time series, into rolling (optional) windows and returns as list of arrays and the number of windows.
    
    Parameters
    ----------
    x : list, np.ndarray, pd.Series
        The time series array to window.
    size : int
        Window size
    gap : int 
        Gap size.
    sample_rate : int
        Size and gap will be multiplied by the given sample rate
        allowing you to specify those in seconds instead of samples.
    rolling : bool
        Use rolling windows. 
        If False:
            Will grab "size * sample_rate" elements greedily.
            Be aware of the gap setting that defaults to 1.
    reverse_direction : bool
        Start from the end of the array instead of the beginning.
        Does not change order of elements within windows.
    discard_shorts: bool
        If the given array is shorter than size*sample_rate,
        return (np.Nan,np.Nan) if (True) or (x,0) if (False).


    Returns
    -------
    List of np.ndarrays, number of windows

    """
    
    _= check_instance(x)
    x = convert_to_type(x, 'np.ndarray')

    assert isinstance(size, int), "size must be an integer"
    assert isinstance(gap, int), "gap must be an integer"
    assert isinstance(sample_rate, int), "sample_rate must be an integer"
    assert isinstance(rolling, bool), "rolling must be a bool"
    assert isinstance(reverse_direction, bool), "reverse_direction must be a bool"
    assert isinstance(discard_shorts, bool), "discard_shorts must be a bool"
    
    assert size >= 1, "size must be at least 1"
    assert sample_rate >= 1, "sample_rate must be at least 1"
    if rolling:
        assert gap >= 1, "gap must be at least 1 when creating rolling windows"


    # How many samples per file?
    n_samples = sample_rate*size
    gap_samples = gap*sample_rate
    
    # If the array is too short
    if len(x) < n_samples:
        if discard_shorts:
            return(np.NaN,np.NaN)
        else:
            return(x, 0)


    if rolling:
        n_windows = np.int32((len(x)-n_samples) / gap_samples) + 1
        if reverse_direction:
            stims = [x[len(x)-stimuli*gap_samples-n_samples:len(x)-stimuli*gap_samples] \
                     for stimuli in range(n_windows)]
        else:
            stims = [x[stimuli*gap_samples:stimuli*gap_samples+n_samples] \
                     for stimuli in range(n_windows)]
    else:
        modulus = len(x) % (n_samples + gap_samples)
        n_windows = (len(x) - modulus) / (n_samples + gap_samples)
        n_windows = np.int32(n_windows)

        # If we have enough samples for a window, just not the final gap
        if modulus >= n_samples:
            n_windows += 1
        
        if reverse_direction:
            stims = [x[len(x)-(stimuli+1)*n_samples-stimuli*gap_samples:
                     len(x)-(stimuli)*n_samples-stimuli*gap_samples] \
                     for stimuli in range(n_windows)]
        else:
            stims = [x[stimuli*n_samples+stimuli*gap_samples:
                     (stimuli+1)*n_samples+stimuli*gap_samples] \
                     for stimuli in range(n_windows)]

    return(stims, n_windows)



