"""
@author: ludvigolsen
"""

from typing import List, Tuple, Union, cast
import numpy as np
import pandas as pd
from utipy.utils.check_instance import check_instance
from utipy.utils.convert_to_type import convert_to_type

# TODO: Cythonize


def window(
    x: Union[list, np.ndarray, pd.Series],
    size: int = 2,
    gap: int = 1,
    sample_rate: int = 1,
    rolling: bool = True,
    reverse_direction: bool = False,
    discard_shorts: bool = True,
) -> Tuple[List[np.ndarray], int]:
    """

    Splits array, e.g., time series, into rolling (optional) windows and returns as list of arrays and the number of windows.

    Parameters
    ----------
    x : list, np.ndarray, pd.Series
        The time series array to window.
    size : int
        Window size
    gap : int
        Gap size.
    sample_rate : int
        Size and gap will be multiplied by the given sample rate
        allowing you to specify those in seconds instead of samples.
    rolling : bool
        Use rolling windows.
        If False:
            Will grab "size * sample_rate" elements greedily.
            Be aware of the gap setting that defaults to 1.
    reverse_direction : bool
        Start from the end of the array instead of the beginning.
        Does not change order of elements within windows.
    discard_shorts: bool
        If the given array is shorter than size*sample_rate,
        return ([],0) if (True) or ([x],0) if (False).

    Returns
    -------
    List of np.ndarrays, number of windows

    """

    _ = check_instance(x)
    x = cast(np.ndarray, convert_to_type(x, "np.ndarray"))

    if not isinstance(size, int):
        raise ValueError("size must be an integer")
    if not isinstance(gap, int):
        raise ValueError("gap must be an integer")
    if not isinstance(sample_rate, int):
        raise ValueError("sample_rate must be an integer")
    if not isinstance(rolling, bool):
        raise ValueError("rolling must be a bool")
    if not isinstance(reverse_direction, bool):
        raise ValueError("reverse_direction must be a bool")
    if not isinstance(discard_shorts, bool):
        raise ValueError("discard_shorts must be a bool")

    if size < 1:
        raise ValueError("size must be at least 1")
    if sample_rate < 1:
        raise ValueError("sample_rate must be at least 1")
    if gap < 0:
        raise ValueError(f"gap was negative: {gap}")
    if rolling and gap < 1:
        raise ValueError("gap must be at least 1 when creating rolling windows")

    # How many samples per file?
    n_samples = sample_rate * size
    gap_samples = gap * sample_rate

    # If the array is too short
    if len(x) < n_samples:
        if discard_shorts:
            return [], 0
        else:
            return [x], 0

    if rolling:
        n_windows = np.int32((len(x) - n_samples) / gap_samples) + 1
        if reverse_direction:
            stims = [
                x[
                    len(x) - stimuli * gap_samples - n_samples : len(x)
                    - stimuli * gap_samples
                ]
                for stimuli in range(n_windows)
            ]
        else:
            stims = [
                x[stimuli * gap_samples : stimuli * gap_samples + n_samples]
                for stimuli in range(n_windows)
            ]
    else:
        modulus = len(x) % (n_samples + gap_samples)
        n_windows = (len(x) - modulus) / (n_samples + gap_samples)
        n_windows = np.int32(n_windows)

        # If we have enough samples for a window, just not the final gap
        if modulus >= n_samples:
            n_windows += 1

        if reverse_direction:
            stims = [
                x[
                    len(x) - (stimuli + 1) * n_samples - stimuli * gap_samples : len(x)
                    - (stimuli) * n_samples
                    - stimuli * gap_samples
                ]
                for stimuli in range(n_windows)
            ]
        else:
            stims = [
                x[
                    stimuli * n_samples + stimuli * gap_samples : (stimuli + 1)
                    * n_samples
                    + stimuli * gap_samples
                ]
                for stimuli in range(n_windows)
            ]

    return stims, n_windows
