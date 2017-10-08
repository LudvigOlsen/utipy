Changelog
--------

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
