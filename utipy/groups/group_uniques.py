#!/usr/bin/env 
# -*- coding: utf-8 -*-
"""
@author: ludvigolsen
"""

import pandas as pd
from .methods.l_sizes import _l_sizes
from .methods.n_dist import _n_dist

def group_uniques(data, n, col, method = 'n_dist'):
    """
    Adds grouping factor to given
    dataframe by unique values in col.
    
    """

    data = data.copy()
    
    # Get unique IDs
    uniques = list(set(data[col]))

    # Create grouping factor from unique IDs
    if method == 'n_dist':
        all_group_ids = _n_dist(uniques, n, randomize = True)
    elif method == 'l_sizes':
        all_group_ids = _l_sizes(uniques, n, randomize = True)
    
    # Create dictionary with unique values
    # and groups
    groups_dict = {}
    groups_dict[col] = uniques
    groups_dict['group'] = all_group_ids
    
    # Create dataframe with unique IDs and the
    # grouping factor
    df_grouped = pd.DataFrame(groups_dict)
    
    # Merge and return the given dataframe with the
    # new grouping factor
    return(data.merge(df_grouped, on = col, how='outer'))
    