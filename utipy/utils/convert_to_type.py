"""
@author: ludvigolsen
"""

import numpy as np
import pandas as pd

def convert_to_type(data, data_type):
    
    """
    Converts (if necessary) data into either of these data types:
     - list
     - tuple
     - np.ndarray
     - pd.Series
     - pd.DataFrame
    
    """
    if data_type not in ["list", "tuple", "np.ndarray", "pd.Series", "pd.DataFrame"]:
        raise ValueError(f"`data_type` was unknown: '{data_type}'.")

    # Convert 
    if data_type == 'list' and not isinstance(data, list):
        return list(data)
    elif data_type == 'tuple' and not isinstance(data, tuple):
        return tuple(data)
    elif data_type == 'np.ndarray' and type(data).__module__ != np.__name__:
        return np.asarray(data)    
    elif data_type == 'pd.Series' and not isinstance(data, pd.Series):
        return pd.Series(data)
    elif data_type == 'pd.DataFrame' and not isinstance(data, pd.DataFrame):
        try:
            return pd.DataFrame(data)
        except:
            return pd.DataFrame({'x':data})
    return data
        