"""
@author: ludvigolsen
"""

import numpy as np
from utipy.measures.iqr import _iqr

# For pandas objects

def _extended_describe(Series):
    """
    Adds median and IQR to `pandas.Series.describe()`.
    Only works for numeric series.
    """
    desc = Series.describe()
    desc['median'] = np.median(Series)
    desc['IQR'] = _iqr(Series)
    return desc
    