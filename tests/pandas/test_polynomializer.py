# Testing pandas.polynomializer

import utipy as ut
import numpy as np
import pandas as pd


def test_polynomializer_DataFrame():

    df = pd.DataFrame(
        {
            'a': [1, 2, 3, 4, 5],
            'b': [2, 3, 4, 5, 6],
            'c': ['a', 'b', 'c', 'd', 'e']
        }
    )
    polynomialized = ut.polynomializer(df, degree=3, exclude=['c'])

    out_df = pd.DataFrame(
        {
            'a': [1, 2, 3, 4, 5],
            'b': [2, 3, 4, 5, 6],
            'c': ['a', 'b', 'c', 'd', 'e'],
            'a_poly2': [1, 4, 9, 16, 25],
            'b_poly2': [4, 9, 16, 25, 36],
            'a_poly3': [1, 8, 27, 64, 125],
            'b_poly3': [8, 27, 64, 125, 216]
        },
        columns=['a', 'b', 'c',
                 'a_poly2', 'b_poly2',
                 'a_poly3', 'b_poly3'])

    assert polynomialized.equals(out_df)


def test_polynomializer_Series():

    x1 = pd.Series([1, 2, 3, 4])

    # Notice, when polynomializer converts to dataframe
    # the column name is automatically 'x' and not 'x1'
    polynomialized = ut.polynomializer(x1, degree=2)
    out_df = pd.DataFrame(
        {
            'x': [1, 2, 3, 4, ],
            'x_poly2': [1, 4, 9, 16]
        },
        columns=['x', 'x_poly2'])
    assert polynomialized.equals(out_df)
