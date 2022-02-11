#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import numpy as np
import pandas as pd

def convert_to_type(data, data_type):
    
    """
    Converts (if necessary) data into either of these data types:
    list
    tuple
    np.ndarray
    pd.Series
    pd.DataFrame
    
    """
    if data_type == 'list' and not isinstance(data, list):
        try:
            return(list(data))
        except:
            raise(TypeError("Could not convert to list"))
    
    elif data_type == 'tuple' and not isinstance(data, tuple):
        try:
            return(tuple(data))
        except:
            raise(TypeError("Could not convert to tuple"))
    
    elif data_type == 'np.ndarray' and type(data).__module__ != np.__name__:
        try:
            return(np.asarray(data))
        except:
            raise(TypeError("Could not convert to numpy.ndarray"))
            
    elif data_type == 'pd.Series' and not isinstance(data, pd.Series):
        try:
            return(pd.Series(data))
        except:
            raise(TypeError("Could not convert to pandas.Series"))
    
    elif data_type == 'pd.DataFrame' and not isinstance(data, pd.DataFrame):
        try:
            try:
                return(pd.DataFrame(data))
            except:
                return(pd.DataFrame({'x':data}))
        except:
            raise(TypeError("Could not convert to pandas.DataFrame"))
    else:
        return(data)
        