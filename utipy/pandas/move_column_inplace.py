
import pandas as pd


def move_column_inplace(df: pd.DataFrame, col: str, pos: int):
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
    col = df.pop(col)
    df.insert(pos, col.name, col)
