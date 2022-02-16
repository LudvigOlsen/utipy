
import pytest
from utipy.utils.recursive_attributes import recursive_getattr, recursive_hasattr, recursive_setattr


def test_recursive_getattr_examples():

    # Create class 'B' with a dict 'c' with the member 'd'
    class B:
        def __init__(self):
            self.c = {
                "d": 1
            }
    # Add to a dict 'a'
    a = {"b": B()}

    # Get the value of 'd'
    assert recursive_getattr(a, "b.c.d") == 1

    # Get default value when not finding an attribute
    assert recursive_getattr(a, "b.o.p", default="not found") == "not found"

    # object is None
    assert recursive_getattr(None, "b.o.p", allow_none=True) is None
    with pytest.raises(TypeError):
        assert recursive_getattr(None, "b.o.p", allow_none=False)


def test_recursive_hasattr_examples():

    # Create class 'B' with a dict 'c' with the member 'd'
    class B:
        def __init__(self):
            self.c = {
                "d": 1
            }
    # Add to a dict 'a'
    a = {"b": B()}

    # Check presence of the member 'd'
    assert recursive_hasattr(a, "b.c.d")

    # Fail to find member 'o'
    assert not recursive_hasattr(a, "b.o.p")

    # object is None
    assert not recursive_hasattr(None, "b.o.p", allow_none=True)
    with pytest.raises(TypeError):
        assert recursive_hasattr(None, "b.o.p", allow_none=False)


def test_recursive_setattr_examples():

    # Create class 'B' with a dict 'c' with the member 'd'
    class B:
        def __init__(self):
            self.c = {
                "d": 1
            }
    # Add to a dict 'a'
    a = {"b": B()}

    # Set the value of 'd'
    recursive_setattr(a, "b.c.d", 2)
    # Check new value of d
    assert recursive_getattr(a, "b.c.d") == 2
