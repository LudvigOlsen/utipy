
import pandas as pd

from utipy.pandas.move_column_inplace import move_column_inplace


def test_move_column_inplace():
    df = pd.DataFrame(
        {
            'a': [1, 2, 3, 4, 5],
            'b': [2, 3, 4, 5, 6],
            'c': ['a', 'b', 'c', 'd', 'e']
        }
    )
    assert all(df.columns == ["a", "b", "c"])
    move_column_inplace(df, "b", 0)
    assert all(df.columns == ["b", "a", "c"])