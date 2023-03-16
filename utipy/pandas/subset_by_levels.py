#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

from typing import List
import pandas as pd

# TODO Could this not be easily done with group_by -> split?
# Consider refactoring or removing this function


def subset_by_levels(
    data: pd.DataFrame,
    cat_col: str,
    drop_cat_col: bool = False
) -> List[pd.DataFrame]:
    """
    Subsets dataframe by each level of a categorical column.


    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to subset.
    cat_col : str, int
        Name or index of categorical column to subset by.
    drop_cat_col: bool
        Remove the categorical column from each subset.


    Returns
    -------
    list of pd.DataFrames


    Examples
    --------

    >>> df = pd.DataFrame({'a': [1,2,3,4],
    ...                    'b': [2,3,4,5],
    ...                    'c': ['a','b','a','b']})
    >>> subset_by_levels(df, cat_col = 'c')

    """

    # Find the unique values (levels)
    # in the given categorical column
    levels = list(set(data[cat_col]))

    # Create subsets for each level
    # Saved as a list of dataframes
    subsets = [pd.DataFrame(data[data[cat_col] == l]) for l in levels]

    # Remove cat_col
    if drop_cat_col:
        subsets = [d.drop(cat_col, axis=1) for d in subsets]

    # Return subsets
    return subsets
