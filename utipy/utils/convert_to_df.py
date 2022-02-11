"""
@author: ludvigolsen
"""

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
        return data, data_type

    elif isinstance(data, pd.Series):
        data_type = 'pd.Series'
        data = pd.DataFrame({'x': data})

    elif type(data).__module__ == np.__name__:
        try:
            data = pd.DataFrame(data)
            data_type = 'np.ndarray'

        except:
            raise TypeError(f"`data` is the wrong format: '{type(data)}'.")
    else:
        raise TypeError("`data` is the wrong format.")

    return data, data_type
