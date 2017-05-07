#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import pandas as pd
import numpy as np
from random import sample

from . import resemble
from utipy.array.blend import blend
from utipy.helpers.convert_to_df import convert_to_df

def distort(data, 
            distribution = 'uniform', 
            amount = 1,
            size = 1,
            randomize_original = False,
            exclude = None,
            label_column = None, 
            keep_labels = True,
            new_label = 'noise', 
            append = False):
    
    """Distort data in pandas DataFrame

    Generates data that resembles the original data by using descriptors
    of each column to create and sample from a specified distribution.
    This new data is blended with the original data to taste.


    Parameters
    ----------
    data : pd.DataFrame
        The data to distort.
    distribution : str
        Distribution to sample from.
            'uniform'
                between min. and max.
            'gaussian'
                from mean and std.
            'robust gaussian'
                from median and IQR.
            'poisson' 
                NOT IMPLEMENTED PROPERLY YET.
            'shuffle'
                shuffles original data.
    amount : float
        Blend rate. Amount of generated data to keep.   
        Percentage between 0-1
            0: Keep only original data.
            1: Keep only generated data.
            0.1: 10% generated / 90% original.
        A value in-between 0-1 will result in integers becoming floats.
    size : float
        Size of data to return relative to original dataframe.
        Percentage between 0-1.
        Observations are randomly sampled.
    randomize_original : bool
        Should the values of the inputted data be randomized?
    exclude : list of strings
        Names of columns not to generate.
        Are filled with NaN.
    label_column : str
        Name of column with labels.
        Used when having a categorical 
        column that should either keep
        its labels or get a new label.
    keep_labels : bool
        Leave label column untouched.
    new_label : str
        Label to fill label column with.
        Used when keep_labels is False.
    append : bool
        Append output to original data


    Returns
    -------
    pd.DataFrame
        Distorted data. Either by itself or appended to original data.


    """
    
    
    ## Check inputs
    # exclude must be array not scalar

    # If data is a pd.Series or np.ndarray
    # Make into a dataframe and 
    # remember what type it originally was
    data, data_type = convert_to_df(data)
    
    ## Subsets

    # Select excluded and included columns
    
    if exclude is not None:
    
        # Select column names to regenerate as noise
        included_cols = [col for col in data.columns if col not in np.append(label_column, exclude)]
        
    else:
        
        # Select columns to regenerate as noise
        included_cols = data.columns[data.columns != label_column]
        
    # Get included columns from column names
    data_included = data.filter(items = included_cols)
    
    
    ## Regenerate included columns as noise
    
    data_regenerated = data_included.apply(resemble, distribution = distribution)
    

    ## Blend 
    
    # Based on amount, blend the two signals
    if amount != 1:
        
        data_blended = pd.concat([blend(data[v], data_regenerated[v], amount = amount) for \
                                  v in data_regenerated.columns], axis = 1)
        
    else:
        
        data_blended = data_regenerated


    ## Label column

    if label_column is not None:

        if keep_labels:

            data_blended[label_column] = data[label_column]

        else:

            # Add label column with the new label
            data_blended[label_column] = new_label
        
    
    ## Set excluded columns to NaN
    
    if exclude is not None:
        
        # Create empty dataframe the shape of [rows, excluded cols]
        null_data = pd.DataFrame(np.zeros([len(data), len(exclude)]))#, columns = exclude)
        
        # Set 0'es to NaN
        null_data[null_data == 0] = 'nan'
        
        # Set column names 
        null_data.columns = exclude
        
        # Add columns to the blended dataset
        data_blended = pd.concat([data_blended, null_data], axis = 1)


    ## Reorder

    # Get columns in original order
    data_ordered = data_blended.filter(items = data.columns)


    ## Cut to 'size'

    if randomize_original:
        # Sample indices from range 0: n rows
        keep_indices = sample(range(0,len(data)), int(len(data)*size))
        
        # Get the rows with the sampled indices
        keep_data = data_ordered.iloc[keep_indices]
    
    else:

        keep_data = data_ordered[:int(len(data)*size)]
        
    
    # Append
    if append:
        # Make sure they are the same size
        return(pd.concat([data[:len(keep_data)], keep_data])) 
    else:
        return(keep_data)
    
    
    