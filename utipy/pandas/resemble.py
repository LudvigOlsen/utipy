#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:14:44 2017

@author: ludvigolsen
"""

from utipy.helpers import _extended_describe
import numpy as np
from random import shuffle

def resemble(Series, distribution = 'uniform'):
    
    """
    distribs:   uniform, gaussian, poisson, robust gaussian (median/IQR),
                shuffle
                Perhaps even: brown noise, pink noise, etc. 
    
    
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
        
        generated = np.random.uniform(low=desc['min'], high=desc['max'], size=desc['count'])
    
    elif distribution == 'gaussian':
        
        generated = np.random.normal(loc=desc['mean'], scale=desc['std'], size=desc['count'])
        
    elif distribution == 'robust gaussian':
        
        generated = np.random.normal(loc=desc['median'], scale=desc['IQR'], size=desc['count'])
    
    elif distribution == 'poisson':
        
        # CHECK UP ON THIS ONE! SHOULD THERE BE A MIN / MAX? 
        # HOW DOES POISSON REALLY WORK?
        generated = np.random.poisson(lam=desc['max'], size=desc['count'])
        
    elif distribution == 'shuffle':
        
        generated = shuffle(Series)
        
    # Change back to original dtype
    generated = generated.astype(desc['dtype'])
    
    return(generated)
    