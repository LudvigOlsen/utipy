#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

from utipy.helpers import _extended_describe
import numpy as np
from random import shuffle

def resemble(Series, distribution = 'uniform'):
    
    """Generate resembling Series

    Generates data that resembles the original data by using descriptors
    of the Series to create and sample from a specified distribution.


    Parameters
    ----------
    Series : pd.Series
        The Series to resemble.
    distribution : str
        Distribution to sample from.
            'uniform'
                between min. and max.
            'gaussian'
                from mean and std.
            'robust gaussian'
                from median and IQR.
            'poisson' 
                NOT IMPLEMENTED PROPERLY YET.
            'shuffle'
                shuffles original data.
    

    Returns
    -------
    pd.Series


    """
    
    
    # Do a tryCatch on describe to
    # see if it's a character vector or other
    # type that it can't describe.
    # Alternatively just check if input is int, double or float?
    # Get descriptors

    # Check for NaNs


    # Get description of Series
    desc = _extended_describe(Series)

    
    if distribution == 'uniform':
        
        generated = np.random.uniform(low=desc['min'], high=desc['max'], size=int(desc['count']))
    
    elif distribution == 'gaussian':
        
        generated = np.random.normal(loc=desc['mean'], scale=desc['std'], size=int(desc['count']))
        
    elif distribution == 'robust gaussian':
        
        generated = np.random.normal(loc=desc['median'], scale=desc['IQR'], size=int(desc['count']))
    
    elif distribution == 'poisson':
        
        # CHECK UP ON THIS ONE! SHOULD THERE BE A MIN / MAX? 
        # HOW DOES POISSON REALLY WORK?
        generated = np.random.poisson(lam=desc['max'], size=int(desc['count']))
        
    elif distribution == 'shuffle':
        
        generated = shuffle(Series)
        
    # Change back to original dtype
    generated = generated.astype(desc['dtype'])
    
    return(generated)
    