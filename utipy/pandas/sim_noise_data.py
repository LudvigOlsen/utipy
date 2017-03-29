
import pandas as pd
import numpy as np
from random import sample

from . import regenerate_as_noise

# Different name?
def sim_noise_data(data, distribution = 'uniform', 
                 size = 1,
                 exclude = None,
                 label_column = None, new_label = 'noise', 
                 append = False):
    
    """
    data :          pd.DataFrame
    distribution :  uniform, gaussian, poisson, 
                    robust gaussian (median/IQR),
                    shuffle
    size :          0-1 (percentage of size of data)
    exclude :       List of columns to exclude
                    Will be filled with NaN
                    Given in []
    label_column :  Categorical variable
                    Will be filled with new label
    new_label :     Label to put in label_column
                  
    """
    
    ## Check inputs
    # exclude must be array not scalar
    
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
    
    data_regenerated = data_included.apply(regenerate_as_noise, distribution = distribution)
    
    # Add label column with the new label
    data_regenerated[label_column] = new_label
    
    
    ## Set excluded columns to NaN
    
    if exclude is not None:
        
        # Create empty dataframe the shape of [rows, excluded cols]
        null_data = pd.DataFrame(np.zeros([len(data), len(exclude)]))#, columns = exclude)
        
        # Set 0'es to NaN
        null_data[null_data == 0] = 'nan'
        
        # Set column names 
        null_data.columns = exclude
        
        # Add columns to the regenerated dataset
        data_regenerated = pd.concat([data_regenerated, null_data], axis = 1)
        
    # Get columns in original order
    data_ordered = data_regenerated.filter(items = data.columns)
    
    ## Cut to 'size'
    # Sample indices from range 0: n rows
    keep_indices = sample(range(0,len(data)), int(len(data)*size))
    
    # Get the rows with the sampled indices
    keep_data = data_ordered.iloc[keep_indices]
    
    
    # Append
    if append:
        return(pd.concat([data, keep_data]))
    else:
        return(keep_data)
    
    
    