"""
@author: ludvigolsen
"""

import numpy as np


def _iqr(x):
    """
    Calculate InterQuartile Range
    """
    q75, q25 = np.percentile(x, [75, 25])
    return q75 - q25
