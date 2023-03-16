"""
@author: ludvigolsen
"""

from typing import Union
import numpy as np
import pandas as pd
from utipy.utils.check_instance import check_instance
from utipy.utils.convert_to_type import convert_to_type


def blend(
        x1: Union[list, np.ndarray, pd.Series], 
        x2: Union[list, np.ndarray, pd.Series], 
        amount: float = 0.5
    ) -> Union[list, np.ndarray, pd.Series]:
    """
    Blend two arrays

    Parameters
    ----------
    x1 : list, np.ndarray, pd.Series
        The first array.
    x2 : list, np.ndarray, pd.Series
        The second array.
    amount : float
        Blend rate. 
        Percentage between 0-1
            0: Keep only x1.  
            1: Keep only x2.  
            0.1: 10% x2 / 90% x1.  
        A value in-between 0-1 will result in integers becoming floats.

    Returns
    -------
    list, np.ndarray, pd.Series
        Blended array with type of the original (x1)

    Examples
    --------
    
    >>> x1 = [1,2,3,4,5]  
    >>> x2 = [4,5,6,7,8]  
    >>> blend(x1, x2, amount = 0.5)  
    [2.5,3.5,4.5,5.5,6.5]

    """

    # Get instance types (np.ndarray, list, pd.Series)
    instance_type = check_instance(x1)

    x1_weighted = np.multiply(x1, (1 - amount))
    x2_weighted = np.multiply(x2, amount)

    blended = x1_weighted + x2_weighted

    # Convert to original type (np.ndarray, list, pd.Series)
    return convert_to_type(blended, instance_type)
