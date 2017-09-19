#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import pandas as pd
import numpy as np
import warnings

from utipy.helpers.convert_to_df import convert_to_df


def polynomializer(data, degree = 2, suffix = '_poly', exclude = []):
    
    """Creates polymonial features.
    Adds suffix with information on which degree a column represents.
    

    Parameters
    ----------
    data : pd.DataFrame
        The data to add polynomial features to.
    degree : int
        How many degrees to add.
    suffix: str
        Text between column name and degree number.
        Added to the new columns.
    exclude: list
        List of column names to exclude, e.g. non-numeric
        columns.


    Returns
    -------
    pd.DataFrame with added polynomial features / columns.


    Examples
    --------
    
    Uncomment code to run.
    
    # df = pd.DataFrame({'a': [1,2,3,4,5],
    #                    'b': [2,3,4,5,6],
    #                    'c': ['a','b','c','d','e']})
    # polynomializer(df, degree = 3, exclude = ['c'])

    """
    
    # Create copy of data
    data = data.copy()
    
    data,_ = convert_to_df(data)

    if exclude != []:

        cols_include = [c for c in data.columns if c not in exclude]
        data_include =  data.filter(items = cols_include)
    
    else:

        data_include = data


    try:
        # Create dataframes with exponential columns
        polynomialized = [data_include ** deg for deg in range(degree+1)[1:]]
    
    except:

        # This exception is most likely seen
        # because a column in data_include is NOT numeric.
        # So we exclude non-numeric columns, warn the user
        # and try again.

        numeric_data = data_include.select_dtypes(include=[np.number])
        
        # Get excluded columns and add to exclude
        auto_excluded = [i for i in data_include.columns if i not in numeric_data.columns] 
        exclude = np.concatenate([exclude, auto_excluded])

        if len(auto_excluded) != 0:
            warnings.warn("Excluded {} non-numeric columns.".format(len(auto_excluded)))

            try:
                # Create dataframes with exponential columns
                polynomialized = [numeric_data ** deg for deg in range(degree+1)[1:]]
            except ValueError:
                print("Something went wrong when creating polynomials.")
                raise
            except TypeError:
                print("Something went wrong when creating polynomials.")
                raise
            except:
                print("Something went wrong when creating polynomials.")
                raise
        
        else:
            print("Something went wrong when creating polynomials.")
            raise

    # Function for adding suffix to column names
    def suffixicate(df, deg):
        if deg != 0:
            return(df.add_suffix("{}{}".format(suffix, deg+1)))
        else:
            return(df)
    
    # Add suffices to dataframes
    polynomialized = map(lambda df, deg: suffixicate(df,deg), 
                         polynomialized, range(degree))
    
    # Combine dataframes
    polynomialized = pd.concat(polynomialized, axis = 1)    

    # Combine processed data with excluded data
    data_all = pd.concat([data.filter(items = exclude), polynomialized], axis = 1)

    ## Reorder 

    # First get all the new column names
    new_cols = [c for c in polynomialized.columns if c not in data.columns]

    # Append old and new column names
    all_columns_sorted = np.append(data.columns, new_cols)

    # Reorder dataframe
    data_ordered = data_all.filter(items = all_columns_sorted)

    
    return(data_ordered)
