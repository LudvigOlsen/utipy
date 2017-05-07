# Testing pandas.drop

import utipy as ut
import numpy as np
import pandas as pd

def test_drop_DF_columns():

    df = pd.DataFrame({'a': [1,2,3,4,5],
                       'b': [2,3,4,5,6],
                       'c': ['a','b','c','d','e'],
                       's': ['a','a','a','b','c'],
                       'na': [np.nan, np.nan, 3,4,1],
                       'infs': [np.inf, np.nan, 3,4,1],
                       'zero': [0,0,0,0,1],
                       'zeros': [0,0,0,0,0]},
                       columns = ['a', 'b','c', 's','na','infs','zero','zeros'])
    
    # Check one or two dataframes, then just check the colnames
    

    # Columns

    droppedNaN = ut.drop(data = df, 
                         value = 'NaN',
                         thresh = 0,
                         direction = '>')

    assert (droppedNaN.columns == ['a', 'b','c', 's','zero','zeros']).all()


    droppedinf = ut.drop(data = df, 
                         value = 'inf',
                         thresh = 0,
                         direction = '>')

    assert (droppedinf.columns == ['a', 'b','c', 's', 'na', 'zero','zeros']).all()

    dropped0 = ut.drop(data = df, 
                         value = 0,
                         thresh = 0.9,
                         direction = '>')

    assert (dropped0.columns == ['a', 'b','c', 's','na','infs','zero']).all()

    dropped08 = ut.drop(data = df, 
                         value = 0,
                         thresh = 0.8,
                         direction = '>=')

    assert (dropped08.columns == ['a', 'b','c', 's','na','infs']).all()

    droppedany = ut.drop(data = df, 
                         value = 'any',
                         thresh = 0.3,
                         direction = '>')

    assert (droppedany.columns == ['a', 'b','c','infs']).all()

    droppednone = ut.drop(data = df, 
                         value = 7,
                         thresh = 1,
                         direction = '>')

    assert (droppednone.columns == ['a', 'b','c', 's','na','infs','zero','zeros']).all()
    assert (droppednone.dtypes == df.dtypes).all()
    # exclude
    droppedexc = ut.drop(data = df, 
                         value = 'NaN',
                         thresh = 0,
                         direction = '>',
                         exclude = ['infs'])

    assert (droppedexc.columns == ['a', 'b','c', 's','infs','zero','zeros']).all()

    # include
    droppedinc = ut.drop(data = df, 
                         value = 'NaN',
                         thresh = 0,
                         direction = '>',
                         include = ['infs'])

    assert (droppedinc.columns == ['a', 'b','c', 's','na','zero','zeros']).all()



def test_drop_DF_rows():

    df = pd.DataFrame({'a': [np.inf,np.nan,3,4,5],
                       'b': [2,3,4,5,6],
                       'c': ['a','b','c','d','e'],
                       's': ['a','a','a','b','c'],
                       'na': [np.nan, np.nan, 3,4,1],
                       'infs': [np.inf, np.nan, 3,4,1],
                       'zero': [0,0,0,0,1],
                       'zeros': [0,0,0,0,0]},
                       columns = ['a', 'b','c', 's','na','infs','zero','zeros'])
    
    # Check one or two dataframes, then just check the colnames
    

    # Columns

    droppedNaN = ut.drop(data = df, 
                         axis = 1,
                         value = 'NaN',
                         thresh = 0,
                         direction = '>')

    assert (droppedNaN.columns == ['a', 'b','c', 's','na','infs','zero','zeros']).all()
    assert droppedNaN.shape == (3,8)
    assert (droppedNaN.index.values == np.asarray([2,3,4])).all()


    droppedinf = ut.drop(data = df, 
                         axis = 1,
                         value = 'inf',
                         thresh = 0,
                         direction = '>')

    assert droppedinf.shape == (4,8)
    assert (droppedinf.index.values == np.asarray([1,2,3,4])).all()

    dropped0 = ut.drop(data = df, 
                         axis = 1,
                         value = 0,
                         thresh = 1.5/8, # more than one appearance of 0 (8 columns)
                         direction = '>')

    assert dropped0.shape == (1,8)
    assert (dropped0.index.values == np.asarray([4])).all()


    droppedany = ut.drop(data = df, 
                         axis = 1,
                         value = 'any',
                         thresh = 2./8, # more than two appearances of any value
                         direction = '>')

    assert droppedany.shape == (2,8)
    assert (droppedany.index.values == np.asarray([0,4])).all()
    
    droppednone = ut.drop(data = df, 
                         axis = 1,
                         value = 7,
                         thresh = 1,
                         direction = '>')

    assert droppednone.shape == (5,8)
    assert (droppednone.index.values == np.asarray([0,1,2,3,4])).all()


    # Needs testing / thinking about include and exclude for axis = 1?
    # Do they take indices?

    # assert (droppednone.columns == ['a', 'b','c', 's','na','infs','zero','zeros']).all()
    # assert (droppednone.dtypes == df.dtypes).all()
    # # exclude
    # droppedexc = ut.drop(data = df, 
    #                      axis = 1,
    #                      value = 'NaN',
    #                      thresh = 0,
    #                      direction = '>',
    #                      exclude = ['infs'])

    # assert (droppedexc.columns == ['a', 'b','c', 's','infs','zero','zeros']).all()

    # # include
    # droppedinc = ut.drop(data = df, 
    #                      axis = 1,
    #                      value = 'NaN',
    #                      thresh = 0,
    #                      direction = '>',
    #                      include = ['infs'])

    # assert (droppedinc.columns == ['a', 'b','c', 's','na','zero','zeros']).all()











