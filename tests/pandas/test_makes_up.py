# Testing pandas.makes_up

import utipy as ut
import numpy as np
import pandas as pd


def test_makes_up_Series():

    x0 = pd.Series([0, 0, 0, 0, 0])
    xNaN = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])
    xinf = pd.Series([np.inf, np.inf, np.inf, np.inf, np.inf])
    x6 = pd.Series([1, 2, 3, 4, 5, 6, 6, 6, 6, 6])

    assert ut.makes_up(x0, 0, thresh=1, direction='==')
    assert not ut.makes_up(x0, 0, thresh=1, direction='<')
    assert ut.makes_up(x0, 0, thresh=0.5, direction='>')

    assert ut.makes_up(xNaN, 'NaN', thresh=1, direction='==')
    assert not ut.makes_up(xNaN, 'NaN', thresh=1, direction='<')
    assert ut.makes_up(xNaN, 'NaN', thresh=0.5, direction='>')

    assert ut.makes_up(xinf, 'inf', thresh=1, direction='==')
    assert not ut.makes_up(xinf, 'inf', thresh=1, direction='<')
    assert ut.makes_up(xinf, 'inf', thresh=0.5, direction='>')

    assert ut.makes_up(xinf, 'any', thresh=1, direction='==')
    assert not ut.makes_up(xinf, 'any', thresh=1, direction='<')
    assert ut.makes_up(xinf, 'any', thresh=0.5, direction='>')
    assert ut.makes_up(xNaN, 'any', thresh=0.5, direction='>')

    assert not ut.makes_up(x6, 6, thresh=1, direction='==')
    assert ut.makes_up(x6, 6, thresh=1, direction='<')
    assert not ut.makes_up(x6, 6, thresh=0.5, direction='>')
    assert not ut.makes_up(x6, 6, thresh=0.5, direction='<')
    assert ut.makes_up(x6, 6, thresh=0.5, direction='==')
    assert ut.makes_up(x6, 6, thresh=0.3, direction='>')


def test_makes_up_ndarray():

    x0 = np.asarray([0, 0, 0, 0, 0])
    xNaN = np.asarray([np.nan, np.nan, np.nan, np.nan, np.nan])
    xinf = np.asarray([np.inf, np.inf, np.inf, np.inf, np.inf])
    x6 = np.asarray([1, 2, 3, 4, 5, 6, 6, 6, 6, 6])

    assert ut.makes_up(x0, 0, thresh=1, direction='==')
    assert not ut.makes_up(x0, 0, thresh=1, direction='<')
    assert ut.makes_up(x0, 0, thresh=0.5, direction='>')

    assert ut.makes_up(xNaN, 'NaN', thresh=1, direction='==')
    assert not ut.makes_up(xNaN, 'NaN', thresh=1, direction='<')
    assert ut.makes_up(xNaN, 'NaN', thresh=0.5, direction='>')

    assert ut.makes_up(xinf, 'inf', thresh=1, direction='==')
    assert not ut.makes_up(xinf, 'inf', thresh=1, direction='<')
    assert ut.makes_up(xinf, 'inf', thresh=0.5, direction='>')

    assert ut.makes_up(xNaN, 'any', thresh=0.5, direction='>')

    assert not ut.makes_up(x6, 6, thresh=1, direction='==')
    assert ut.makes_up(x6, 6, thresh=1, direction='<')
    assert not ut.makes_up(x6, 6, thresh=0.5, direction='>')
    assert not ut.makes_up(x6, 6, thresh=0.5, direction='<')
    assert ut.makes_up(x6, 6, thresh=0.5, direction='==')
    assert ut.makes_up(x6, 6, thresh=0.3, direction='>')


def test_makes_up_list():

    x0 = [0, 0, 0, 0, 0]
    xNaN = [np.nan, np.nan, np.nan, np.nan, np.nan]
    xinf = [np.inf, np.inf, np.inf, np.inf, np.inf]
    x6 = [1, 2, 3, 4, 5, 6, 6, 6, 6, 6]

    assert ut.makes_up(x0, 0, thresh=1, direction='==')
    assert not ut.makes_up(x0, 0, thresh=1, direction='<')
    assert ut.makes_up(x0, 0, thresh=0.5, direction='>')

    assert ut.makes_up(xNaN, 'NaN', thresh=1, direction='==')
    assert not ut.makes_up(xNaN, 'NaN', thresh=1, direction='<')
    assert ut.makes_up(xNaN, 'NaN', thresh=0.5, direction='>')

    assert ut.makes_up(xinf, 'inf', thresh=1, direction='==')
    assert not ut.makes_up(xinf, 'inf', thresh=1, direction='<')
    assert ut.makes_up(xinf, 'inf', thresh=0.5, direction='>')

    assert not ut.makes_up(x6, 6, thresh=1, direction='==')
    assert ut.makes_up(x6, 6, thresh=1, direction='<')
    assert not ut.makes_up(x6, 6, thresh=0.5, direction='>')
    assert not ut.makes_up(x6, 6, thresh=0.5, direction='<')
    assert ut.makes_up(x6, 6, thresh=0.5, direction='==')
    assert ut.makes_up(x6, 6, thresh=0.3, direction='>')
