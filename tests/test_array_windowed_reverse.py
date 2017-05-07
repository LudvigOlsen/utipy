# Testing array.windowed_reverse 

import utipy as ut
import numpy as np
import pandas as pd

def test_windowed_reverse_list():

	x = [1,20,23,44,5,62,3]

	rev1 = ut.windowed_reverse(x, wsize = 1)
	rev2 = ut.windowed_reverse(x, wsize = 2)
	rev3 = ut.windowed_reverse(x, wsize = 3)
	
	assert rev1 == x
	assert rev2 == [20,1,44,23,62,5,3]
	assert rev3 == [23,20,1,62,5,44,3]

def test_windowed_reverse_ndarray():

	x = np.asarray([1,20,23,44,5,62,3])

	rev1 = ut.windowed_reverse(x, wsize = 1)
	rev2 = ut.windowed_reverse(x, wsize = 2)
	rev3 = ut.windowed_reverse(x, wsize = 3)
	
	assert (rev1 == x).all()
	assert (rev2 == np.asarray([20,1,44,23,62,5,3])).all()
	assert (rev3 == np.asarray([23,20,1,62,5,44,3])).all()

def test_windowed_reverse_Series():

	x = pd.Series([1,20,23,44,5,62,3])

	rev1 = ut.windowed_reverse(x, wsize = 1)
	rev2 = ut.windowed_reverse(x, wsize = 2)
	rev3 = ut.windowed_reverse(x, wsize = 3)
	
	assert (rev1 == x).all()
	assert (rev2 == pd.Series([20,1,44,23,62,5,3])).all()
	assert (rev3 == pd.Series([23,20,1,62,5,44,3])).all()