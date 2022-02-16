# Testing array.blend

import utipy as ut
import numpy as np
import pandas as pd


def test_blend_list():

    x1 = [1, 2, 3, 4, 5, 6]
    x2 = [2, 3, 4, 5, 6, 7]

    blended0 = ut.blend(x1, x2, amount=0)
    blended1 = ut.blend(x1, x2, amount=1)
    blended05 = ut.blend(x1, x2, amount=.5)

    assert blended0 == x1
    assert blended1 == x2
    assert blended05 == [1.5, 2.5, 3.5, 4.5, 5.5, 6.5]


def test_blend_ndarray():

    x1 = np.asarray([1, 2, 3, 4, 5, 6])
    x2 = np.asarray([2, 3, 4, 5, 6, 7])

    blended0 = ut.blend(x1, x2, amount=0)
    blended1 = ut.blend(x1, x2, amount=1)
    blended05 = ut.blend(x1, x2, amount=.5)

    assert (blended0 == x1).all()
    assert (blended1 == x2).all()
    assert (blended05 == np.asarray([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])).all()


def test_blend_Series():

    x1 = pd.Series([1, 2, 3, 4, 5, 6])
    x2 = pd.Series([2, 3, 4, 5, 6, 7])

    blended0 = ut.blend(x1, x2, amount=0)
    blended1 = ut.blend(x1, x2, amount=1)
    blended05 = ut.blend(x1, x2, amount=.5)

    assert (blended0 == x1).all()
    assert (blended1 == x2).all()
    assert (blended05 == pd.Series([1.5, 2.5, 3.5, 4.5, 5.5, 6.5])).all()
