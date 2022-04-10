
from typing import Any, Callable, Optional, Union


class Messenger:

    def __init__(self, verbose: bool = True, msg_fn: Callable = print, indent: Union[int, None] = 0) -> None:
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

        Examples
        --------

        Uncomment code to run.

        # # Initialize print messenger
        # # By default, the `print` function is used
        # printer = Messenger(verbose=True, indent=4)

        # # Adds default indentation 
        # printer("anything printable")
        # >> "    anything printable"

        # # We can set a specific indentation for a call
        # printer("overriding indentation for call", indent=0)
        # >> "overwriting indentation for call"

        # # Logging messenger
        # import logging
        # logging.basicConfig()
        # # Create logger
        # _logger = logging.getLogger("Mr.Logger")
        # # Set level to INFO so we see the output
        # _logger.setLevel(logging.INFO)
        # Initialize logger that messages info
        # logger = Messenger(verbose=True, indent=0, msg_fn=_logger.info)

        # # Log something
        # logger("anything printable", "- even multiple arguments")
        # >> "INFO  Mr.Logger:script.py:xz  anything printable - even multiple arguments"

        """
        # Check types
        assert isinstance(verbose, bool)
        assert callable(msg_fn)
        assert isinstance(indent, int)

        self.verbose = verbose
        self.msg_fn = msg_fn
        self.indent = indent

    def __call__(self, *args: Any, verbose: Union[None, bool] = None, indent: Union[None, int] = None) -> None:
        """
        Perform messaging using `self.msg_fn`.

        Parameters
        ----------
        verbose : bool
            Whether to perform the messaging for this specific call.
        indent : int
            Number of whitespaces to indent the message in this specific call.
        """
        if verbose is None:
            verbose = self.verbose
        if indent is None:
            indent = self.indent
        msg_if(*args, verbose=verbose, indent=indent, msg_fn=self.msg_fn)

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
        self.indent += indent
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
        if self.indent - indent < 0:
            raise ValueError(
                f"Subtracting {indent} positions would give a "
                "negative indentation level. Can maximally subtract "
                f"{self.indent} positions.")
        self.indent -= indent
        return self


def msg_if(*args: Any, verbose: bool, indent: int = 0, msg_fn: Callable = print) -> None:
    """
    Message (print/log/..) the given `args` arguments when `verbose` is enabled.

    Parameters
    ----------
    *args : Any
        Parts to print/log. Anything printable (i.e. with a `__str__` method).
    verbose : bool
        Whether to perform the messaging.
    indent : int
        Number of whitespaces to indent the message.
    msg_fn : callable
        Function for performing the messaging.
        E.g. `print` or `log.info`.
    """
    assert indent >= 0
    if verbose:
        subtract_1 = len(args) > 0
        indent_str = "".join(
            [" " for _ in range(max(0, indent - int(subtract_1)))]
        )
        msg_fn(_args_to_string(indent_str, *args))


def _args_to_string(*args):
    return " ".join([str(a) for a in args])


def check_messenger(messenger: Optional[Callable]):
    """
    Check that `messenger` is a `utipy.Messenger` object or `None`, 
    in which case a `utipy.Messenger` with `verbose=False` is returned.

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
