utipy
--------

Utility functions for python.

Alpha stage. Subject to change. 

> https://pypi.python.org/pypi/utipy/     

> $ pip install utipy  
  

### Pandas operations

| Function                | Description |
|:------------------------|:------------|
| `makes_up()`            | Is a Series made up of a specific value (more than / less than / equal to a threshold) ? |
| `drop()`                | Drop rows / columns of dataframe based on the percentile appearance of a specified value |
| `polynomializer()`      | Add polynomials to numeric columns, i.e. v1, v1^2, v1^3, ... |
| `resemble()`            | Generate a Series resembling another Series |
| `move_column_inplace()` | Move a column to a specified index |

### Data grouping

| Function      | Description |
|:--------------|:------------|
| `group()`     | Create grouping factors with different methods |
| `partition()` | Create balanced partitions for train/test      |
| `fold()`      | Create balanced folds for cross-validation     |

### Array operations

| Function             | Description |
|:---------------------|:------------|
| `blend()`            | Blend two arrays of same length  |
| `windowed_reverse()` | Reverse array within windows     |
| `window()`           | Split array into rolling windows |
| `nan_stats()`, `print_nan_stats()` | Get NaN statistics |

### Time operations

| Class        | Description |
|:-------------|:------------|
| `StepTimer`  | Time a step of code in a `with` context |
| `Timestamps` | Record and keep track of timepoints     |

### Path operations

| Class/Function   | Description |
|:-----------------|:------------|
| `InOutPaths`     | Keep track of in-/out paths with checks, directory creation, and a print summary |
| `mk_dir()`       | Create directory if it doesn't exist, with messaging of the created path         | 

### Other utilities

| Class/Function      | Description |
|:--------------------|:------------|
| `Messenger`         | Simplify messaging (print/log) with verbosity and indentation  |
| `recursive_getattr` | Get object attributes/dict members recursively, given by dot-separated names |
| `recursive_setattr` | Set object attribute/dict member by recursive lookup, given by dot-separated names. |
| `recursive_hasattr` | Check whether recursive object attributes/dict members exist. |


TODO
 - Add documentation
 - Add brown noise, pink noise, etc. as 'distributions' in resemble()
 - Add argument checks
