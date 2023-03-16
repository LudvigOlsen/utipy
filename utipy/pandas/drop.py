"""
@author: ludvigolsen
"""

from typing import Callable, Optional, Union, List
import pandas as pd
from numbers import Number

from utipy.utils.messenger import Messenger, check_messenger
from .makes_up import makes_up


def drop(
    data: pd.DataFrame,
    value: Union[str, Number] = 'NaN',
    thresh: float = 0,
    direction: str = '>',
    axis: int = 0,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    copy: bool = True,
    messenger: Optional[Callable] = Messenger(
        verbose=True, indent=0, msg_fn=print)
) -> pd.DataFrame:
    """
    Drop rows or columns from pandas DataFrame based on values.

    Drop rows / columns if specific value, or any value, is represented too much, too little, etc.

    Commands:
        'Drop [axis] if [value] appears [direction] than [thresh] percent of the time.'
    E.g.:
        'Drop columns if 0 appears more than 90 percent of the time.'
        'Drop rows if *any* value appears exactly 77 percent of the time.'


    Parameters
    ----------
    data : pd.DataFrame
        The data to distort.
    value : str / int / float
        The value to match.
            Regular value, 
            'any',
            'NaN',
            'inf'
    thresh : float
        Threshold.
        Percentage between 0-1.
    direction : str
        Operator sign for comparison.
            '>', '<', '>=', '<=', '=='.
    axis : int
        0 for columns, 1 for rows.
    include : list of strings
        Names of columns / indices of rows to search within. 
        None means ALL are included unless otherwise specified, see *exclude*.
    exclude : list of strings
        Names of columns / indices of rows NOT to search within.
        None means no columns/rows are excluded unless otherwise specified, see *include*.
    messenger : `utipy.Messenger` or None
        A `utipy.Messenger` instance used to print/log/... information.
        When `None`, no printing/logging is performed.
        The messenger determines the messaging function (e.g. `print`)
        and potential indentation.


    Returns
    -------
    pd.DataFrame


    Examples
    --------

    Remove all rows with any NaNs in dependent variable 'y'
    >>> drop(data, value = 'NaN', axis = 1, thresh = 0, 
    ...      direction = '>', cols = ['y'])

    Remove all columns with only 1 unique value.
    I.e. the same value in 100% of the rows.
    >>> drop(data, value = 'any', axis = 0, thresh = 1, 
    ...      direction = '==')

    Remove all columns that have less than 30% NaNs
    >>> drop(data, value = 'NaN', axis = 0, thresh = 0.3, 
    ...      direction = '<')

    """

    # Check messenger (always returns Messenger instance)
    messenger = check_messenger(messenger)

    if value is None:
        raise ValueError('value cannot be None.')

    if axis not in [0, 1]:
        raise ValueError("`axis` must be 0 or 1")

    # Create copy of dataframe
    if copy:
        data = data.copy()

    if exclude is not None and include is not None:
        raise ValueError("Either include or exclude must be None.")

    # Columns
    if axis == 0:

        if exclude is not None:
            # Create include list
            include = [col for col in data.columns if col not in exclude]

        if include is not None:
            # Subset dataframe to only work on included cols
            data_cols = data.filter(items=include)

            # Find columns / rows to drop
            to_drop = _find_exceeders(data_cols, value,
                                      thresh, direction,
                                      axis=axis)
        else:
            # Find columns / rows to drop
            to_drop = _find_exceeders(data, value, thresh,
                                      direction, axis=axis)

        # Drop columns
        messenger(f'Dropped {len(to_drop)} columns.')

        return data.drop(to_drop, axis=1)

    # Rows
    elif axis == 1:
        # Find columns / rows to drop
        to_drop = _find_exceeders(data, value, thresh,
                                  direction, axis=axis)

        # Remove indices not in include or in exclude
        # TODO use sets instead
        if exclude is not None:
            to_drop = [i for i in to_drop if i not in exclude]
        elif include is not None:
            to_drop = [i for i in to_drop if i in include]

        # Drop rows
        messenger(f'Dropped {len(to_drop)} rows.')

        return data.drop(data.index[to_drop], axis=0)


# Wrapper for calling makes_up - for finding columns / rows to drop
def _find_exceeders(data, value, thresh, direction, axis):
    """Internal wrapper function for calling makes_up()"""

    # Notice:
    # pd apply() passes the Series as objects, even
    # when it's the columns it's working with!

    if axis not in [0, 1]:
        raise ValueError("`axis` must be 0 or 1")

    exceeders = data.apply(
        makes_up,
        axis=axis,
        value=value,
        thresh=thresh,
        direction=direction
    )

    if axis == 0:
        # Find columns to drop
        to_drop = [
            col for col, exceedes in
            zip(data.columns, exceeders)
            if exceedes
        ]

    elif axis == 1:
        # Find rows to drop
        to_drop = [
            row for row, exceedes in
            zip(data.index, exceeders)
            if exceedes
        ]

    return to_drop
