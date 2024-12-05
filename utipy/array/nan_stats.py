

from typing import Callable, Optional, Tuple, Union
import numpy as np
import pandas as pd

from utipy.utils.messenger import Messenger, check_messenger


def print_nan_stats(
        x: Union[np.ndarray, pd.DataFrame],
        message: str,
        messenger: Optional[Callable] = Messenger(
            verbose=True, indent=0, msg_fn=print),
        indent: Optional[int] = None) -> None:
    """
    Print statistics about NaNs in an array.

    Parameters
    ----------
    x : `numpy.ndarray` or `pandas.DataFrame`
        The array / data frame to count NaNs in.
    message : str
        The message prior to the stats. Full message becomes:
            `indentation + message + ": " + num NaNs (percentage)` 
    messenger : `utipy.Messenger` or None
        A `utipy.Messenger` instance used to print/log/... information.
        When `None`, no printing/logging is performed.
        The messenger determines the messaging function (e.g., `print` or `log.info`)
        and indentation when `indent` is `None`.
    indent : int
        Indentation of message. When `None`, indentation is determined by `messenger`.
    """
    messenger = check_messenger(messenger)
    num_nans, perc = nan_stats(x)
    messenger(f"{message}: {num_nans} ({perc}%)", indent=indent)


def nan_stats(x: Union[np.ndarray, pd.DataFrame]) -> Tuple[int, float]:
    """
    Get statistics about NaNs in an array.

    Parameters
    ----------
    x : `numpy.ndarray`
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
