utipy
--------

Utility functions for python.

Pandas and array operations. Data grouping, folding, and partitioning.

Alpha stage. Subject to change. 

> https://pypi.python.org/pypi/utipy/     

> $ pip install utipy  
  

 - Pandas operations
 	- Is a Series made up of a specific value (more than / less than / equal to a threshold) ?
 	- Drop rows / columns of dataframe based on the percentile appearance of a specified value
 	- Subset by each level of a categorical column
 	- Add polynomials to numeric columns, i.e. v1, v1^2, v1^3, ...
 	- Generate a Series resembling another Series

 - Data grouping
 	- Create grouping factor from different methods
 	- Balanced partitions for train/test
 	- Balanced folds for cross-validation

 - Array operations
 	- Blend two arrays of same length
 	- Reverse array within windows

TODO
 - Add documentation
 - Add brown noise, pink noise, etc. as 'distributions' in resemble()
 - Add argument checks
