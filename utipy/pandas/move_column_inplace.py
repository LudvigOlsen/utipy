
import pandas as pd


def move_column_inplace(df: pd.DataFrame, col: str, pos: int) -> None:
    """
    Move a column to a given column-index position.

    Parameters
    ----------
    df : `pandas.DataFrame`.
    col : str
        Name of column to move.
    pos : int
        Column index to move `col` to.
    """
    assert 0 <= pos < len(df.columns), \
        f"`pos` must be between 0 (incl.) and the number of columns -1. Was {pos}."
    col = df.pop(col)
    df.insert(pos, col.name, col)
