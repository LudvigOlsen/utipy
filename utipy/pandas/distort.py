"""
@author: ludvigolsen
"""

import pandas as pd
import numpy as np
from random import sample
from numbers import Real
from typing import Optional, List

from .resemble import resemble
from utipy.array.blend import blend
from utipy.utils.convert_to_df import convert_to_df

# TODO The label column concept is not properly described


def distort(
    data: pd.DataFrame,
    distribution: str = "uniform",
    amount: float = 1.0,
    size: float = 1.0,
    randomize_original: bool = False,
    exclude: Optional[List[str]] = None,
    label_column: Optional[str] = None,
    keep_labels: bool = True,
    new_label: str = "noise",
    append: bool = False,
) -> pd.DataFrame:
    """
    Distort data in pandas DataFrame

    Generates data that resembles the original data by using descriptors
    of each column to create and sample from a specified distribution.
    This new data is blended with the original data to taste.


    Parameters
    ----------
    data : pd.DataFrame
        The data to distort.
    distribution : str
        Distribution to sample from.
            'uniform'
                between min. and max.
            'gaussian'
                from mean and std.
            'robust gaussian'
                from median and IQR.
            'poisson'
                NOT IMPLEMENTED PROPERLY YET.
            'shuffle'
                shuffles original data.
    amount : float
        Blend rate. Amount of generated data to keep.
        Percentage between 0-1
            0: Keep only original data.
            1: Keep only generated data.
            0.1: 10% generated / 90% original.
        A value in-between 0-1 will result in integers becoming floats.
    size : float
        Size of data to return relative to original dataframe.
        Percentage between 0-1.
        Observations are randomly sampled.
    randomize_original : bool
        Should the values of the inputted data be randomized?
    exclude : list of strings
        Names of columns not to generate.
        Are filled with NaN.
    label_column : str
        Name of column with labels.
        Used when having a categorical
        column that should either keep
        its labels or get a new label.
    keep_labels : bool
        Leave label column untouched.
    new_label : str
        Label to fill label column with.
        Used when keep_labels is False.
    append : bool
        Append output to original data


    Returns
    -------
    pd.DataFrame
        Distorted data. Either by itself or appended to original data.
    """

    # If data is a pd.Series or np.ndarray
    # Make into a dataframe and
    # remember what type it originally was
    data, _ = convert_to_df(data)

    # Validate blend and row-sampling proportions early. Values outside [0, 1]
    # otherwise extrapolate the blend or produce surprising slices.
    _check_fraction(amount, name="amount")
    _check_fraction(size, name="size")

    exclude = _normalize_exclude(exclude)

    if label_column is not None and label_column not in data.columns:
        raise ValueError(f"`label_column` was not in `data.columns`: {label_column}")

    missing_exclude = [col for col in exclude if col not in data.columns]
    if missing_exclude:
        raise ValueError(
            "All columns in `exclude` must exist in `data`. "
            f"Missing: {missing_exclude}"
        )

    # Subsets
    # Select columns to regenerate as noise. Label and excluded columns are
    # handled separately because categorical/object columns cannot be
    # summarized by `resemble()`'s numeric distribution logic.
    protected_cols = set(exclude)
    if label_column is not None:
        protected_cols.add(label_column)
    included_cols = [col for col in data.columns if col not in protected_cols]

    non_numeric_cols = [
        col
        for col in included_cols
        if not pd.api.types.is_numeric_dtype(data[col])
        or pd.api.types.is_bool_dtype(data[col])
    ]
    if non_numeric_cols:
        raise ValueError(
            "Only numeric columns can be distorted. Pass non-numeric columns "
            "as `label_column` or in `exclude`. "
            f"Non-numeric columns: {non_numeric_cols}"
        )

    # Get included columns from column names
    data_included = data.filter(items=included_cols)

    # Regenerate included columns as noise
    data_regenerated = data_included.apply(resemble, distribution=distribution)

    # Blend
    # Based on amount, blend the two signals
    if amount != 1:
        data_blended = pd.concat(
            [
                blend(data[v], data_regenerated[v], amount=amount)
                for v in data_regenerated.columns
            ],
            axis=1,
        )
    else:
        data_blended = data_regenerated

    # Label column
    # TODO Improve the above comment xD
    if label_column is not None:
        if keep_labels:
            data_blended[label_column] = data[label_column]
        else:
            # Add label column with the new label
            data_blended[label_column] = new_label

    # Set excluded columns to NaN
    if exclude:
        # Excluded columns are intentionally blanked out in the distorted
        # rows, while preserving the original index for safe concat alignment.
        null_data = pd.DataFrame(np.nan, index=data.index, columns=exclude)

        # Add columns to the blended dataset
        data_blended = pd.concat([data_blended, null_data], axis=1)

    # Reorder
    # Get columns in original order
    data_ordered = data_blended.filter(items=data.columns)

    # Cut to 'size'
    if randomize_original:
        # Sample indices from range 0: n rows
        keep_indices = sample(range(0, len(data)), int(len(data) * size))

        # Get the rows with the sampled indices
        keep_data = data_ordered.iloc[keep_indices]
    else:
        keep_data = data_ordered[: int(len(data) * size)]

    # Append
    if append:
        # Make sure they are the same size
        # TODO Shouldn't it raise an error instead if they're not?
        return pd.concat([data[: len(keep_data)], keep_data])
    else:
        return keep_data


def _check_fraction(value: float, name: str) -> None:
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError(f"`{name}` must be a number between 0 and 1.")
    if not 0 <= value <= 1:
        raise ValueError(f"`{name}` must be between 0 and 1.")


def _normalize_exclude(exclude: Optional[List[str]]) -> List[str]:
    if exclude is None:
        return []
    if isinstance(exclude, str):
        raise TypeError("`exclude` must be a list of column names, not a string.")
    if not isinstance(exclude, list):
        raise TypeError("`exclude` must be a list of column names.")
    if not all(isinstance(col, str) for col in exclude):
        raise TypeError("All entries in `exclude` must be strings.")
    return exclude
