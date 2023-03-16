"""
@author: ludvigolsen
"""

from typing import Any
import numpy as np
import pandas as pd


def check_instance(data: Any) -> str:
    """
    Checks if data is either:
        list
        tuple
        np.ndarray
        pd.Series
        pd.DataFrame

    """
    if isinstance(data, list):
        return 'list'
    elif isinstance(data, tuple):
        return 'tuple'
    elif type(data).__module__ == np.__name__:
        return 'np.ndarray'
    elif isinstance(data, pd.Series):
        return 'pd.Series'
    elif isinstance(data, pd.DataFrame):
        return 'pd.DataFrame'
    else:
        raise TypeError("Doesn't recognize instance type")
