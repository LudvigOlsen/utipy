
import numpy as np


def has_illegal_chars(s, allowed):
    """
    Check if string contains unallowed characters.

    :param s: String to check characters of.
    :param allowed: List/set of allowed characters to check against.
    :returns: Bool. `True` if `s` contains characters not in 
        `allowed` else `False`.
    """
    return bool(get_illegal_chars(s=s, allowed=allowed))


def get_illegal_chars(s, allowed):
    """
    Get the characters in `s` that are not in `allowed`.

    :param s: String to check characters of.
    :param allowed: List/set of allowed characters to check against.
    :returns: Set of characters from `s` that was not found in `allowed`.
    """
    return set(s).difference(set(allowed))


def parse_ranges_from_string(ranges_string, default_fn_name="max", arg_name='ranges_string'):
    """
    Parse a string with ranges (e.g. frequency ranges) and potential function names.
    Note that ranges are inclusive for both the start and end indices.

    Example:
        The string '1,max(2-5),sum(7-10),13-15' has: 
            - 4 (all-inclusive) ranges (1, 2-5, 7-10, 13-15)
            - Aggregation functions (max, sum) for the second and third ranges
                - The other ranges (1, 13-15) will use the default function (see `default_fn_name`).
        Output:
            1) Frequencies: 
               > [[1], [2,3,4,5], [7,8,9,10], [13,14,15]]
            2) Functions (given `default_fn_name` is `np.max`):
               > [np.max, np.max, np.sum, np.max] 
            3) Function names:
               > ['max', 'max', 'sum', 'max']

    :param ranges_string: String for specifying inclusive integer ranges and potential aggregation functions.
        E.g. '1,max(2-5),sum(7-10),13-15'
    :param default_fn_name: Name of the function to return for ranges that do not specify one.
        One of: {'max', 'min', 'mean', 'sum', 'std'}.
    :param arg_name: The argument name for `ranges_string` for error messages.
    :returns: 
        1) List of lists with integer frequencies for each range.
        2) List of functions - one for each range.
        3) List of function names - one for each range.
    """

    # Trim whitespace
    ranges_string = ranges_string.replace(' ', '')

    # Separate ranges
    range_strings = ranges_string.split(",")

    # Remove empty strings
    range_strings = [s for s in range_strings if s]

    # Separate range string from function name
    # I.e. 'max(1,2,3)' becomes ('max', '1,2,3')
    # When no function name is given, fn name is `None`
    range_strings, fn_names = zip(*[
        separate_function_name(s, msg_prefix='A range string')
        for s in range_strings
    ])

    # Check function names are valid
    for fn_name in fn_names:
        assert fn_name is None or fn_name in ["max", "min", "mean", "sum", "std"], \
            (f"The extracted function name ('{fn_name}') was not one of allowed names: "
             "{'max', 'min', 'mean', 'sum', 'std'}.")

    # Check illegal characters in range strings
    combined_range_strings = ''.join(range_strings)
    allowed_chars = ['-'] + [f'{c}' for c in range(10)]
    illegal_chars = get_illegal_chars(
        s=combined_range_strings,
        allowed=allowed_chars
    )
    if len(illegal_chars) != 0:
        raise ValueError((
            f"`{arg_name}` contained illegal characters. "
            "Can only contain numbers (0-9) and characters (',' '-') "
            f"but contained: {', '.join(illegal_chars)}."
        ))

    # Get frequencies for each range (lists of integers)
    freq_ranges = [_string_to_range(s) for s in range_strings]

    # Map function names to their numpy functions
    fn_name_to_fn = {
        "max": np.max,
        "min": np.min,
        "mean": np.mean,
        "sum": np.sum,
        "std": np.std
    }

    # Extract functions

    # Set `None`s to default function name
    fn_names = [n if n is not None else default_fn_name for n in fn_names]

    # Get function for each function name
    fns = [fn_name_to_fn[n] for n in fn_names]

    return freq_ranges, fns, fn_names


def _string_to_range(s):
    if "-" in s:
        min_, max_ = s.split("-")
        return list(range(int(min_), int(max_) + 1))  # Inclusive
    return [int(s)]


# Extract function names
def separate_function_name(s, msg_prefix='A string'):
    """
    Given a string like `'max(1,2,3)'`, split into `['max', '1,2,3']`.
    When no function name is given, the function name is returned as `None`.
    """

    # Check there is a function in the string
    if '(' not in s:
        return s, None

    # Split to ['fn(', 'xxx)']
    parts = s.split('(')

    # We should have 2 parts now
    # else something was wrong with the string
    if len(parts) == 1:
        if s[0] == "(":
            raise ValueError(
                f"{msg_prefix} started with '('. Please add a valid function name. String was: '{s}'")
        if s[-1] == "(":
            raise ValueError(
                f"{msg_prefix} ended with '('. That is not meaningful. String was: '{s}'")
        raise ValueError(
            f"Could not split a range string properly at '('. Please report. String was: '{s}'")
    if len(parts) > 2:
        raise ValueError(
            f"{msg_prefix} had multiple '(' characters: '{s}'")

    # Extract function name
    fn_name = parts[0].lower()

    # Extract argument part
    range_string = parts[1]

    # Remove end paranthesis
    if range_string[-1] == ")":
        range_string = range_string[:-1]

    return range_string, fn_name
