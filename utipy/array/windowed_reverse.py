"""
@author: ludvigolsen
"""

from typing import Union, cast
import numpy as np
import pandas as pd
from utipy.utils.check_instance import check_instance
from utipy.utils.convert_to_type import convert_to_type


def windowed_reverse(
    x: Union[list, np.ndarray, pd.Series], wsize: int = 2
) -> Union[list, np.ndarray, pd.Series]:
    """Reverse / flip windows of array

    Parameters
    ----------
    x : list, np.ndarray, pd.Series
        The array to reverse
    wsize: int
        Window size

    Returns
    -------
    list, np.ndarray, pd.Series
        Window reversed array with the type of the original

    Examples
    --------
        x = 1,2,3,4,5,6; wsize = 2 returns 2,1,4,3,6,5
        x = 1,2,3,4,5,6; wsize = 3 returns 3,2,1,6,5,4
    """

    # Get instance type (np.ndarray, list, pd.Series)
    instance_type = check_instance(x)

    if not isinstance(wsize, int):
        raise TypeError(f"wsize must in int but had type: {type(wsize)}")
    if wsize < 1:
        raise ValueError(f"wsize must be at least 1 but was: {wsize}")

    # Window and reverse
    reversed_windows = [x[pos : pos + wsize][::-1] for pos in range(len(x))[::wsize]]

    # Flatten windows
    flattened_array = np.concatenate(reversed_windows)

    # Convert to original type (np.ndarray, list, pd.Series)
    return cast(
        Union[list, np.ndarray, pd.Series],
        convert_to_type(flattened_array, instance_type),
    )
