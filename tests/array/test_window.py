# Testing array.window

import utipy as ut
import numpy as np


def test_window_list_not_rolling():

    x1 = [1, 2, 3, 4, 5, 6]

    w1, nw1 = ut.window(x1, size=3, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w1_ = [np.array([1, 2, 3]), np.array([4, 5, 6])]

    w2, nw2 = ut.window(x1, size=4, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w2_ = [np.array([1, 2, 3, 4])]

    w3, nw3 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w3_ = [np.array([1, 2, 3, 4])]

    w4, nw4 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=False, reverse_direction=True,
                        discard_shorts=True)
    w4_ = [np.array([3, 4, 5, 6])]

    w5, nw5 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w5_ = [np.array([1, 2]), np.array([4, 5])]

    w6, nw6 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=False, reverse_direction=True,
                        discard_shorts=True)
    w6_ = [np.array([5, 6]), np.array([2, 3])]

    w7, nw7 = ut.window(x1, size=7, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w7_ = []

    w8, nw8 = ut.window(x1, size=7, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=False)
    w8_ = [np.asarray(x1)]

    assert np.array_equal(w1, w1_)
    assert np.array_equal(w2, w2_)
    assert np.array_equal(w3, w3_)
    assert np.array_equal(w4, w4_)
    assert np.array_equal(w5, w5_)
    assert np.array_equal(w6, w6_)
    assert np.array_equal(w7, w7_)
    assert np.array_equal(w8, w8_)

    assert nw1 == 2
    assert nw2 == 1
    assert nw3 == 1
    assert nw4 == 1
    assert nw5 == 2
    assert nw6 == 2
    assert nw7 == 0
    assert nw8 == 0


def test_window_ndarray_not_rolling():

    x1 = np.array([1, 2, 3, 4, 5, 6])

    w1, nw1 = ut.window(x1, size=3, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w1_ = [np.array([1, 2, 3]), np.array([4, 5, 6])]

    w2, nw2 = ut.window(x1, size=4, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w2_ = [np.array([1, 2, 3, 4])]

    w3, nw3 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w3_ = [np.array([1, 2, 3, 4])]

    w4, nw4 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=False, reverse_direction=True,
                        discard_shorts=True)
    w4_ = [np.array([3, 4, 5, 6])]

    w5, nw5 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w5_ = [np.array([1, 2]), np.array([4, 5])]

    w6, nw6 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=False, reverse_direction=True,
                        discard_shorts=True)
    w6_ = [np.array([5, 6]), np.array([2, 3])]

    w7, nw7 = ut.window(x1, size=7, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w7_ = []

    w8, nw8 = ut.window(x1, size=7, gap=0, sample_rate=1,
                        rolling=False, reverse_direction=False,
                        discard_shorts=False)
    w8_ = [x1]

    assert np.array_equal(w1, w1_)
    assert np.array_equal(w2, w2_)
    assert np.array_equal(w3, w3_)
    assert np.array_equal(w4, w4_)
    assert np.array_equal(w5, w5_)
    assert np.array_equal(w6, w6_)
    assert np.array_equal(w7, w7_)
    assert np.array_equal(w8, w8_)

    assert nw1 == 2
    assert nw2 == 1
    assert nw3 == 1
    assert nw4 == 1
    assert nw5 == 2
    assert nw6 == 2
    assert nw7 == 0
    assert nw8 == 0


def test_window_list_rolling():

    x1 = [1, 2, 3, 4, 5, 6]

    w1, nw1 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w1_ = [np.array([1, 2]), np.array([2, 3]),
           np.array([3, 4]), np.array([4, 5]),
           np.array([5, 6])]

    w2, nw2 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=True,
                        discard_shorts=True)
    w2_ = [np.array([5, 6]), np.array([4, 5]),
           np.array([3, 4]), np.array([2, 3]),
           np.array([1, 2])]

    w3, nw3 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w3_ = [np.array([1, 2, 3, 4])]

    w4, nw4 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=True, reverse_direction=True,
                        discard_shorts=True)
    w4_ = [np.array([3, 4, 5, 6])]

    w5, nw5 = ut.window(x1, size=4, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w5_ = [np.array([1, 2, 3, 4]),
           np.array([2, 3, 4, 5]),
           np.array([3, 4, 5, 6])]

    w6, nw6 = ut.window(x1, size=4, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=True,
                        discard_shorts=True)
    w6_ = [np.array([3, 4, 5, 6]),
           np.array([2, 3, 4, 5]),
           np.array([1, 2, 3, 4])]

    assert np.array_equal(w1, w1_)
    assert np.array_equal(w2, w2_)
    assert np.array_equal(w3, w3_)
    assert np.array_equal(w4, w4_)
    assert np.array_equal(w5, w5_)
    assert np.array_equal(w6, w6_)

    assert nw1 == 5
    assert nw2 == 5
    assert nw3 == 1
    assert nw4 == 1
    assert nw5 == 3
    assert nw6 == 3


def test_window_ndarray_rolling():

    x1 = np.array([1, 2, 3, 4, 5, 6])

    w1, nw1 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w1_ = [np.array([1, 2]), np.array([2, 3]),
           np.array([3, 4]), np.array([4, 5]),
           np.array([5, 6])]

    w2, nw2 = ut.window(x1, size=2, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=True,
                        discard_shorts=True)
    w2_ = [np.array([5, 6]), np.array([4, 5]),
           np.array([3, 4]), np.array([2, 3]),
           np.array([1, 2])]

    w3, nw3 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w3_ = [np.array([1, 2, 3, 4])]

    w4, nw4 = ut.window(x1, size=4, gap=3, sample_rate=1,
                        rolling=True, reverse_direction=True,
                        discard_shorts=True)
    w4_ = [np.array([3, 4, 5, 6])]

    w5, nw5 = ut.window(x1, size=4, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w5_ = [np.array([1, 2, 3, 4]),
           np.array([2, 3, 4, 5]),
           np.array([3, 4, 5, 6])]

    w6, nw6 = ut.window(x1, size=4, gap=1, sample_rate=1,
                        rolling=True, reverse_direction=True,
                        discard_shorts=True)
    w6_ = [np.array([3, 4, 5, 6]),
           np.array([2, 3, 4, 5]),
           np.array([1, 2, 3, 4])]

    assert np.array_equal(w1, w1_)
    assert np.array_equal(w2, w2_)
    assert np.array_equal(w3, w3_)
    assert np.array_equal(w4, w4_)
    assert np.array_equal(w5, w5_)
    assert np.array_equal(w6, w6_)

    assert nw1 == 5
    assert nw2 == 5
    assert nw3 == 1
    assert nw4 == 1
    assert nw5 == 3
    assert nw6 == 3


def test_window_sample_rate():

    x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    w1, nw1 = ut.window(x1, size=2, gap=1, sample_rate=2,
                        rolling=True, reverse_direction=False,
                        discard_shorts=True)
    w1_ = [np.array([1, 2, 3, 4]),
           np.array([3, 4, 5, 6]),
           np.array([5, 6, 7, 8]),
           np.array([7, 8, 9, 10]),
           np.array([9, 10, 11, 12])]

    w2, nw2 = ut.window(x1, size=2, gap=1, sample_rate=2,
                        rolling=False, reverse_direction=False,
                        discard_shorts=True)
    w2_ = [np.array([1, 2, 3, 4]),
           np.array([7, 8, 9, 10])]

    assert np.array_equal(w1, w1_)
    assert np.array_equal(w2, w2_)
    assert nw1 == 5
    assert nw2 == 2
