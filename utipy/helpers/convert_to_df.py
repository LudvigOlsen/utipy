#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import warnings
import numpy as np
import pandas as pd

def convert_to_df(data):
    """
    Checks the type of data
    If it is not a pd.DataFrame it 
    attempts to convert to pd.DataFrame
    
    """
    
    data_type = 'pd.DataFrame'
    if isinstance(data, pd.DataFrame):
        return(data, data_type)

    elif isinstance(data, pd.Series):
        data_type = 'pd.Series'
        data = pd.DataFrame({'x':data})

    elif type(data).__module__ == np.__name__:
        
        # warnings.warn("'data' is a numpy object. Will attempt conversion to pandas.DataFrame")
        try:
            data = pd.DataFrame(data)
            data_type = 'np.ndarray'

        except:
            raise TypeError("'data' is the wrong format.")      
    else:
        raise TypeError("'data' is the wrong format.")
        
            
    return(data, data_type)