

from typing import Tuple, Union
import numpy as np
import pandas as pd


def print_nan_stats(x: Union[np.ndarray, pd.DataFrame], message: str, indent: int = 4) -> None:
    """
    Print statistics about NaNs in an array.

    Parameters
    ----------
    x : numpy.ndarray or pandas.DataFrame
        The array / data frame to count NaNs in.
    message : str
        The message prior to the stats. Full message becomes:
            `indentation + message + ": " + num NaNs (percentage)` 
    indent : int
        How many whitespaces to indent the message.
    """
    assert indent >= 0
    num_nans, perc = nan_stats(x)
    indent_str = "".join([" " for _ in range(indent)])
    print(f"{indent_str}{message}: {num_nans} ({perc}%)")


def nan_stats(x: Union[np.ndarray, pd.DataFrame]) -> Tuple[int, float]:
    """
    Get statistics about NaNs in an array.

    Parameters
    ----------
    x : numpy.ndarray
        A numpy array.

    Returns
    -------
    int
        Number of NaNs in `x`.
    float
        Percentage of `x` that was NaN. 
        Between 0 and 100.
    """
    num_nans = np.count_nonzero(np.isnan(x))
    perc = np.round((num_nans / float(x.size)) * 100, decimals=2)
    return num_nans, perc
