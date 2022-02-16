
import numpy as np

from utipy.array.nan_stats import nan_stats, print_nan_stats


def test_nan_stats(capfd):

    arr = np.array([
        [1, 2, np.nan],
        [1, np.nan, np.nan],
    ])

    assert nan_stats(x=arr) == (3, 50.0)

    print_nan_stats(x=arr, message="NaN statistics for 'arr'", indent=6)
    out, err = capfd.readouterr()
    assert out == "      NaN statistics for 'arr': 3 (50.0%)\n"
