Changelog
--------

v/1.0.* (2025)

 - Fixes removal of nested tmp directories via `IOPaths.rm_tmp_dirs()`.

v/1.0.5 (2025)

 - Updates pyproject.toml for new poetry version.

v/1.0.4 (2025)
 - Fixes `IOPaths.update()` when `other` has empty (`None`) collections.

v/1.0.3 (2024)
 - Fixes empty initialization of `IOPaths`.
 - Adds `__version__` attribute to package.

v/1.0.2 (2024)
 - Adds `add_indent` argument to `Messenger.__call__()`.

v/1.0.1 (2023)
 - Moves `recursive_getattr()`, `recursive_setattr()`, and `recursive_hasattr()`, `recursive_mutattr()` to `nattrs` package.
 - Adds typing to all arguments that did not have it.
 - Converts to poetry packaging backend.

v/1.0.0 (2022)
 - Converted to python 3 only.
 - Adds `recursive_getattr()`, `recursive_setattr()`, and `recursive_hasattr()`, `recursive_mutattr()`.
 - Adds `pandas.move_column_inplace()`.
 - Adds `path.IOPaths` for handling in-/output paths.
 - Adds `path.mk_dir` for creating missing directories.
 - Adds `time.Timestamps` for recording timestamps during runtime.
 - Adds `time.StepTimer` for timing a step in a `with` statement/context.
 - Adds `array.nan_stats()` and `array.print_nan_stats()`.
 - Adds `utils.Messenger` for printing/logging with defaults on verbosity and indentation.

v/0.3.1 (2017)
 - Changes output when arrays are too short in array.window

v/0.3.0
 - Adds array.window

v/0.2.9:
 - minor bugfix

v/0.2.2:
 - pandas.drop gets arguments *include* and *exclude*. This removes *cols* argument.
 - pandas.makes_up get better compatibility with object dtypes. In certain circumstances when a Series is 
 an object, it will convert all elements to str, in order to find infs, NaNs and the special 'any' value
 - Adds more tests

v/0.2.1:
 - pytest testing
 - Adds import bug

v/0.2.0:
 - Adds array.windowed_reverse
 - Adds documentation for lots of functions
