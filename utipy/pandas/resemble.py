"""
@author: ludvigolsen
"""

from typing import Union
from utipy.utils import _extended_describe
import numpy as np
import pandas as pd
from random import shuffle


def resemble(
    x: Union[pd.Series, np.ndarray, list],
    distribution: str = 'uniform'
) -> pd.Series:
    """
    Generate pandas.Series that resembles `x`.

    Generates data that resembles the original data by using descriptors
    of `x` to create and sample from a specified distribution.


    Parameters
    ----------
    x : pandas.Series, numpy.ndarray, list
        The values to resemble.
    distribution : str
        Distribution to sample from. One of:
            'uniform'
                Between min. and max.
            'gaussian'
                From mean and std.
            'robust gaussian'
                From median and IQR.
            'shuffle'
                Shuffles original data.


    Returns
    -------
    pd.Series
    """

    # TODO Do a tryCatch on describe to
    # see if it's a character vector or other
    # type that it can't describe.
    # Alternatively just check if input is int, double or float?
    # Get descriptors

    # TODO Check for NaNs

    # Get description of `x`
    desc = _extended_describe(x)

    if distribution == 'uniform':
        generated = np.random.uniform(
            low=desc['min'],
            high=desc['max'],
            size=int(desc['count'])
        )

    elif distribution == 'gaussian':
        generated = np.random.normal(
            loc=desc['mean'],
            scale=desc['std'],
            size=int(desc['count'])
        )

    elif distribution == 'robust gaussian':
        generated = np.random.normal(
            loc=desc['median'],
            scale=desc['IQR'],
            size=int(desc['count'])
        )

    elif distribution == 'poisson':
        # TODO Check up on this one. Should there be a min/max?
        generated = np.random.poisson(
            lam=desc['max'],
            size=int(desc['count'])
        )

    elif distribution == 'shuffle':
        generated = shuffle(x)

    # Change back to original dtype
    generated = generated.astype(desc['dtype'])

    return generated
