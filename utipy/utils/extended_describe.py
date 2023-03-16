"""
@author: ludvigolsen
"""

from typing import Union
import pandas as pd
import numpy as np
from utipy.measures.iqr import _iqr

# For pandas objects

def _extended_describe(x:Union[pd.Series, np.ndarray, list]) -> dict:
    """
    Adds median and IQR to `pandas.Series.describe()`.
    Only works for numeric series.
    """
    desc = pd.Series(x).describe()
    desc['median'] = np.median(x)
    desc['IQR'] = _iqr(x)
    return dict(desc)
    