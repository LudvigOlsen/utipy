
from utipy.string.letter_strings import letter_strings


def test_letter_strings():

    # n: int, num_chars: Optional[int] = None, upper: bool = False, descending: bool = False
    assert letter_strings(n=3) == ["a", "b", "c"]

    # 2 chars
    ls = letter_strings(n=27)
    assert len(ls) == 27
    assert ls[:3] == ["aa", "ab", "ac"]

    # Start with 1 chars, end with 2
    ls = letter_strings(n=27, num_chars=1)
    assert len(ls) == 27
    assert ls[:3] == ["a", "b", "c"]
    assert ls[-1] == "aa"

    # 3 chars
    ls = letter_strings(n=27, num_chars=3)
    assert len(ls) == 27
    assert ls[:3] == ["aaa", "aab", "aac"]
    assert ls[-1] == "aba"

    # Uppercase
    ls = letter_strings(n=3, upper=True)
    assert ls == ["A", "B", "C"]

    # Descending
    ls = letter_strings(n=3, descending=True)
    assert ls == ["z", "y", "x"]
