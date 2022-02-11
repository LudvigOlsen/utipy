

def move_column_inplace(df, col, pos):
    """
    Move a column to a given column-index position.

    :param df: A `pandas.DataFrame`.
    :param col: Name of column to move.
    :param pos: Column index to move `col` to.
    :returns: `None`. The column is moved inplace.
    """
    col = df.pop(col)
    df.insert(pos, col.name, col)
