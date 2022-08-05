
from functools import partial
from typing import Callable, Union, Any

# TODO Add tests
# TODO What if keys have dots in them? Add escaping of dots somehow?


def recursive_getattr(obj: Union[object, dict], attr: str, default: Any = None, allow_none: bool = False):
    """
    Get object attributes/dict members recursively, given by dot-separated names.

    Pass `attr='x.a.o'` to get attribute "o" of attribute "a" of attribute "x".

    Parameters
    ----------
    obj : object (class instance) or dict
        The object/dict to get attributes/members of.
        These work interchangeably, why "class, dict, class" work as well.
    attr : str
        The string specifying the dot-separated names of attributes/members to get. 
        The most left name is an attribute/dict member of `obj`
        which has the attribute/key given by the second most left name,
        which has the attribute/key given by the third most left name,
        and so on.
    default : Any
        Value to return when one or more of the attributes were not found.
    allow_none : bool
        Whether to allow `obj` to be `None` (in the first call - non-recursively).
        When allowed, such a call would return `None`.

    Returns
    -------
    Any
        One of:
            - The value of the final attribute/dict member.
            - The default value
            - `None`, when `obj` is `None` and `allow_none` is `True`.

    Examples
    --------

    Create class 'B' with a dict 'c' with the member 'd'.

    >>> class B:
    >>>     def __init__(self):
    >>>         self.c = {
    >>>             "d": 1
    >>>         }

    Add to a dict 'a':

    >>> a = {"b": B()}

    Get the value of 'd':

    >>> recursive_getattr(a, "b.c.d")
    1

    Get default value when not finding an attribute:

    >>> recursive_getattr(a, "b.o.p", default="not found")
    "not found"
    """
    if not allow_none and obj is None:
        raise TypeError("`obj` was `None`.")
    return _recursive_getattr(obj=obj, attr=attr, default=default)


def _recursive_getattr(obj: Union[object, dict], attr: str, default: Any = None):
    """
    Modified from:
    https://programanddesign.com/python-2/recursive-getsethas-attr/
    """
    if obj is None:
        return obj
    getter = _dict_getter if isinstance(obj, dict) else getattr
    try:
        left, right = attr.split('.', 1)
    except:
        return getter(obj, attr, default)
    return _recursive_getattr(getter(obj, left, default), right, default)


def recursive_hasattr(obj: Union[object, dict], attr: str, allow_none: bool = False):
    """
    Check whether recursive object attributes/dict members exist.

    Pass `attr='x.a.o'` to check attribute "o" of attribute "a" of attribute "x".

    Parameters
    ----------
    obj : object (class instance) or dict
        The object/dict to check attributes/members of.
        These work interchangeably, why "class, dict, class" work as well.
    attr : str
        The string specifying the dot-separated names of attributes/members
        to get. The most left name is the object/dict which has
        the attribute/key given by the second most left name,
        which has the attribute/key given by the third most left name,
        and so on.
    allow_none : bool
        Whether to allow `obj` to be `None` (in the first call - non-recursively).
        When allowed, such a call would return `False`.

    Returns
    -------
    bool
        Whether the final attribute/dict member exist.

    Examples
    --------

    Create class 'B' with a dict 'c' with the member 'd'

    >>> class B:
    >>>     def __init__(self):
    >>>         self.c = {
    >>>             "d": 1
    >>>         }

    Add to a dict 'a':

    >>> a = {"b": B()}

    Check presence of the member 'd':

    >>> recursive_hasattr(a, "b.c.d")
    True

    Fail to find member 'o':

    >>> recursive_hasattr(a, "b.o.p")
    False
    """
    if not allow_none and obj is None:
        raise TypeError("`obj` was `None`.")
    return _recursive_hasattr(obj=obj, attr=attr)


def _recursive_hasattr(obj: Union[object, dict], attr: str):
    """
    Modified from:
    https://programanddesign.com/python-2/recursive-getsethas-attr/
    """
    if obj is None:
        return False
    getter = _dict_getter if isinstance(obj, dict) else getattr
    has_checker = _dict_has if isinstance(obj, dict) else hasattr
    try:
        left, right = attr.split('.', 1)
    except:
        return has_checker(obj, attr)
    return _recursive_hasattr(getter(obj, left, None), right)


def recursive_setattr(obj: Union[object, dict], attr: str, value: Any, make_missing: bool = False):
    """
    Set object attribute/dict member by recursive lookup, given by dot-separated names.

    Pass `attr='x.a.o'` to set attribute "o" of attribute "a" of attribute "x".

    When `make_missing` is disabled, it requires all but the last attribute/member to already exist.

    Parameters
    ----------
    obj : object (class instance) or dict
        The object/dict to set an attribute/member of a sub-attribute/member of.
        These work interchangeably, why "class, dict, class" work as well.
    attr : str
        The string specifying the dot-separated names of attributes/members. 
        The most left name is an attribute/dict member of `obj`
        which has the attribute/key given by the second most left name,
        which has the attribute/key given by the third most left name,
        and so on. The last name may be non-existent and is the name
        of the attribute/member to set.
    value : Any
        Value to set for the final attribute/member.
    make_missing : bool
        Whether to create a dict for non-existen intermediate attributes/keys. 
        Otherwise, the function will raise an error.

    Examples
    --------

    Create class 'B' with a dict 'c' with the member 'd'

    >>> class B:
    >>>     def __init__(self):
    >>>         self.c = {
    >>>             "d": 1
    >>>         }

    Add to a dict 'a':

    >>> a = {"b": B()}

    Set the value of 'd':

    >>> recursive_setattr(a, "b.c.d", 2)

    Check new value of d:

    >>> recursive_getattr(a, "b.c.d")
    2
    """
    # Modified from:
    # https://programanddesign.com/python-2/recursive-getsethas-attr/

    getter = partial(_dict_getter, default="make" if make_missing else "raise") \
        if isinstance(obj, dict) else (get_or_make_attr if make_missing else getattr)
    setter = _dict_setter if isinstance(obj, dict) else setattr
    try:
        left, right = attr.split('.', 1)
    except:
        return setter(obj, attr, value)
    return recursive_setattr(
        obj=getter(obj, left),
        attr=right,
        value=value,
        make_missing=make_missing
    )


def recursive_mutattr(obj: Union[object, dict], attr: str, fn: Callable):
    """
    Mutate object attribute/dict member by recursive lookup, given by dot-separated names.

    Pass `attr='x.a.o'` to mutate attribute "o" of attribute "a" of attribute "x".

    Parameters
    ----------
    obj : object (class instance) or dict
        The object/dict to mutate an attribute/member of a sub-attribute/member of.
        These work interchangeably, why "class, dict, class" work as well.
    attr : str
        The string specifying the dot-separated names of attributes/members. 
        The most left name is an attribute/dict member of `obj`
        which has the attribute/key given by the second most left name,
        which has the attribute/key given by the third most left name,
        and so on. The last name may be non-existent and is the name
        of the attribute/member to set.
    fn : Callable
        Function that gets existing attribute/key value and 
        returns the new value to be assigned.

    Examples
    --------

    Create class 'B' with a dict 'c' with the member 'd'

    >>> class B:
    >>>     def __init__(self):
    >>>         self.c = {
    >>>             "d": 1
    >>>         }

    Add to a dict 'a':

    >>> a = {"b": B()}

    Mutate `d` with a lambda:

    >>> recursive_mutattr(a, "b.c.d", lambda x: x * 5)

    Check new value of d:

    >>> recursive_getattr(a, "b.c.d")
    10
    """
    old_val = recursive_getattr(obj=obj, attr=attr)
    try:
        new_val = fn(old_val)
    except Exception as e:
        raise RuntimeError(
            f"Failed to apply `fn` to the existing value at `{attr}`: {e}"
        )
    recursive_setattr(obj=obj, attr=attr, value=new_val)


#### Getter/Setter/Checker utils ####

def get_or_make_attr(__o: object, __name: str):
    if not hasattr(__o, __name):
        setattr(__o, __name, {})
    return getattr(__o, __name)


def _dict_getter(obj: dict, key: Any, default: Any):
    if isinstance(default, str):
        if default == "raise":
            return obj[key]
        if default == "make":
            if key not in obj:
                obj[key] = {}
                return obj[key]
    return obj.get(key, default)


def _dict_setter(obj: dict, key: Any, val: Any):
    obj[key] = val


def _dict_has(obj: dict, key: Any):
    return key in obj
