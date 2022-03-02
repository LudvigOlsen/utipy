
from string import ascii_lowercase, ascii_uppercase
import itertools
from typing import List, Optional


def letter_strings(n: int, num_chars: Optional[int] = None, upper: bool = False, descending: bool = False) -> List[str]:
    """
    Generate a sequence of `n` letter strings (aa, ab, ac, ...).

    Parameters
    ----------
    n : int
        Number of letter strings to generate. 
        When `num_chars` is not specified, this also determines the number of
        characters in the strings.
    num_chars : int or None
        The (starting) number of characters in the strings.
        When `None`, this is determined by `n`.
    upper : bool
        Whether to use uppercase letters instead of lowercase.
    descending : bool
        Whether to use letters in descending order.

    Returns
    -------
    list of str
        A list of letter strings. 
        E.g. `['aa', 'ab', 'ac']`.
    """

    # Number of letters in the ascii alphabet
    num_available_letters = 26

    if num_chars is None:
        # Find the necessary number of characters
        # to create the IDs
        num_chars = 1
        while n > num_available_letters ** num_chars:
            num_chars += 1

    # Init letter string generator
    generator = letter_string_generator(
        num_chars=num_chars, upper=upper, descending=descending)

    # Get the n first letter IDs
    return list(itertools.islice(generator, n))


def letter_string_generator(num_chars: int = 1, upper: bool = False, descending: bool = False):
    """
    Letter string generator.

    Parameters
    ----------
    num_chars : int
        The (starting) number of characters in the yielded strings.
    upper : bool
        Whether to use uppercase letters instead of lowercase.
    descending : bool
        Whether to use letters in descending order.

    Yields
    ------
    str
        Given `num_chars` is 2:
            "aa", "ab", "ac", ... "aaa", "aab" ...
    """
    letters = ascii_uppercase if upper else ascii_lowercase
    if descending:
        letters = letters[::-1]
    while True:
        for s in itertools.product(letters, repeat=num_chars):
            yield "".join(s)
        num_chars += 1
