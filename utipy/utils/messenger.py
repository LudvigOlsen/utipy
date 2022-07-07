
from contextlib import contextmanager
from typing import Any, Callable, Optional, Union


class Messenger:

    def __init__(self, verbose: bool = True, msg_fn: Callable = print, indent: Union[int, None] = 0, **kwargs: Any) -> None:
        """
        Wraps a messaging function (print/log.info/...) to simplify messenging.

        The `Messenger` object has specified defaults for whether to perform the messaging (`verbose`), 
        which function to use (`msg_fn`) and how much to indent messages (`indent`). 

        This removes `if` statements before each print/log/... call for checking
        whether we should perform the messaging or not (`verbose`).

        Parameters
        ----------
        verbose : bool
            Default value for whether to perform the messaging.
        msg_fn : callable
            Function for performing the messaging.
            E.g. `print` or `log.info`.
        indent : int
            Default value for number of whitespaces to indent the message.
        kwargs : keyword arguments
            Named arguments to pass to the `msg_fn` by default. 
            The arguments can be overwritten for single calls via the `kwargs` arguments in `__call__()`.
            I.e. by passing them again with different values during the call.
        Examples
        --------

        Initialize print messenger. By default, the `print` function is used. Set an indentation to use.

        >>> printer = Messenger(verbose=True, indent=4)

        Print a string. Notice the added indentation.

        >>> printer("anything printable")
        "    anything printable"

        We can set a specific indentation for a call.

        >>> printer("overriding indentation for call", indent=0)
        "overwriting indentation for call"

        We can pass keyword arguments to the messaging function (here `print()`).

        >>> printer("a string", end=' is all you need')
        "    a string is all you need"

        Create a logging messenger with the logging library.
        Set level to INFO so we see the output.

        >>> import logging
        >>> logging.basicConfig()
        >>> _logger = logging.getLogger("Mr.Logger")
        >>> _logger.setLevel(logging.INFO)
        >>> logger = Messenger(verbose=True, indent=0, msg_fn=_logger.info)

        Log something.

        >>> logger("anything printable", "- even multiple arguments")
        "INFO  Mr.Logger:script.py:xz  anything printable - even multiple arguments"
        """
        # Check types
        assert isinstance(verbose, bool)
        assert callable(msg_fn)
        assert isinstance(indent, int)

        self._verbose = verbose
        self.msg_fn = msg_fn
        self._indent = indent
        self.kwargs = kwargs

    def set_verbose(self, verbose: bool) -> None:
        """
        Set the `verbose` state of the messenger.

        Parameters
        ----------
        verbose : bool
            Default value for whether to perform the messaging.
        """
        self._verbose = verbose

    @property
    def verbose(self) -> bool:
        """
        Get the `verbose` state of the messenger.

        Returns
        -------
        bool
            The default value for whether to perform the messaging.
        """
        return self._verbose

    def set_indent(self, indent: int) -> None:
        """
        Set the indentation of the messenger.

        Parameters
        ----------
        indent : int
            Default value for number of whitespaces to indent the message.
        """
        if indent < 0:
            raise ValueError("`indent` was negative.")
        self._indent = indent

    @property
    def indent(self) -> int:
        """
        Get the indentation setting in the messenger.

        Returns
        -------
        int
            Default number of whitespaces that messages are indented.
        """
        return self._indent

    def __call__(self, *objects: Any, verbose: Union[None, bool] = None, indent: Union[None, int] = None, sep: str = ' ', **kwargs: Any) -> None:
        """
        Perform messaging using `self.msg_fn`.

        Parameters
        ----------
        objects : objects
            Objects to message. Anything printable (i.e. with a `__str__` method).
        verbose : bool
            Whether to perform the messaging for this specific call.
        indent : int
            Number of whitespaces to indent the message in this specific call.
        sep : str
            String used to separate `objects`.
        kwargs : keyword arguments
            Named arguments for the messaging function.
        """
        if verbose is None:
            verbose = self._verbose
        if indent is None:
            indent = self._indent

        # Get kwargs for current call
        call_kwargs = self.kwargs.copy()
        call_kwargs.update(kwargs)

        msg_if(
            *objects,
            verbose=verbose,
            indent=indent,
            msg_fn=self.msg_fn,
            sep=sep,
            **call_kwargs
        )

    def __add__(self, indent: int):
        """
        Add to the current indentation level.

        Parameters
        ----------
        indent : int
            The number of additional positions to indent message.

        Returns
        -------
        `self`
        """
        assert isinstance(indent, int)
        if self._indent + indent < 0:
            raise ValueError(
                f"Subtracting {abs(indent)} positions would give a "
                "negative indentation level. Can maximally subtract "
                f"{self._indent} positions.")
        self._indent += indent
        return self

    def __sub__(self, indent: int):
        """
        Subtract from the current indentation level.

        Parameters
        ----------
        indent : int
            The number of fewer positions to indent message.

        Returns
        -------
        `self`
        """
        assert isinstance(indent, int)
        return self.__add__(indent=indent)

    @contextmanager
    def indentation(self, indent: Optional[int] = None, add_indent: Optional[int] = None) -> None:
        """
        Function to use in `with` statement. Temporarily changes the indentation. 
        The original indentation is restored upon exiting the `with` context.

        Can be used in a nested fashion.

        Parameters
        ----------
        indent : int, optional
            A specific indentation to use within the context.
            Exactly one of `indent` and `add_indent` should be specified.
        add_indent : int, optional
            A relative change in indentation based on the current indentation.
            Exactly one of `indent` and `add_indent` should be specified.

        Yields
        ------
        `None` once.

        Examples
        --------

        Initialize a messenger with `2` indentation spaces.

        >>> msg = Messenger(indent=2)

        Use `4` indentation spaces in a given context. 
        After exiting the `with` context, the indentation 
        is restored to `2` spaces.

        >>> with msg.indentation(indent=4):
        >>>     msg("something")
        "    something"

        Add `4` spaces of indentation to the existing indentation of `2` spaces.

        >>> with msg.indentation(add_indent=4):
        >>>     msg("something")
        "      something"

        Check that indentation is back to `2` spaces.

        >>> msg("something")
        "  something"
        """
        if sum([indent is not None, add_indent is not None]) != 1:
            raise ValueError(
                "Exactly one of {'indent', 'add_indent'} should be specified."
            )

        # Store original indentation, allowing us to restore it
        original_indent = self.indent
        if indent is not None:
            self.set_indent(indent=indent)
        if add_indent is not None:
            self.__add__(indent=add_indent)

        try:
            yield None
        finally:
            self.set_indent(indent=original_indent)


def msg_if(*objects: Any, verbose: bool, indent: int = 0, msg_fn: Callable = print, sep: str = ' ', **kwargs) -> None:
    """
    Message (print/log/..) the given `objects` arguments when `verbose` is enabled.

    Parameters
    ----------
    objects : Any
        Objects to message. Anything printable (i.e. with a `__str__` method).
    verbose : bool
        Whether to perform the messaging.
    indent : int
        Number of whitespaces to indent the message.
    msg_fn : callable
        Function for performing the messaging.
        E.g. `print` or `log.info`.
    sep : str
            String used to separate `objects`.
    kwargs : keyword arguments
        Named arguments for the messaging function.
    """
    assert indent >= 0
    if verbose:
        subtract_1 = len(objects) > 0
        indent_str = "".join(
            [" " for _ in range(max(0, indent - int(subtract_1)))]
        )
        msg_fn(
            _objects_to_string(
                indent_str,
                *objects,
                sep=sep,
            ),
            **kwargs
        )


def _objects_to_string(*args: Any, sep: str = ' '):
    try:
        obj_as_strings = [str(a) for a in args]
    except Exception as e:
        raise RuntimeError(
            f"Failed to convert argument to string: {e}"
        )
    return f"{sep}".join(obj_as_strings)


def check_messenger(messenger: Optional[Callable]):
    """
    Check that `messenger` is a `utipy.Messenger` object or `None`.  
    In the latter case a `utipy.Messenger` with `verbose=False` is returned.

    Parameters
    ----------
    messenger : `utipy.Messenger` or None
        A Messenger instance to check.
        Or `None`, in which case a `utipy.Messenger` with `verbose=False` is returned.

    Returns
    -------
    `utipy.Messenger`
    """
    # Check the messenger function
    if messenger is None:
        messenger = Messenger(verbose=False)
    else:
        assert isinstance(messenger, Messenger)
    return messenger
