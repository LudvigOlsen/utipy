
import random
from string import ascii_letters, digits
from typing import Optional


def random_alphanumeric(size: int, seed: Optional[int] = None) -> str:
    """
    Create a string with random alphanumeric characters.

    Uses it's own `random.Random()` generator why it is
    not affected by external seeds.

    Parameters
    ----------
    size : int 
        Number of characters in the random string.
    seed : int or `None`
        A random seed to use.

    Returns
    -------
    str
        A string of length `size` with random alphanumeric characters.
    """
    # Create a unique random generator
    # which is not affected by seeds elsewhere
    randomgen = random.Random()

    # Set random seed when given
    if seed is not None:
        randomgen.seed(seed)

    # Collect all alphanumeric characters
    char_choices = ascii_letters + digits

    # Pick `size` characters and join to a string
    return ''.join(randomgen.choices(char_choices, k=size))
