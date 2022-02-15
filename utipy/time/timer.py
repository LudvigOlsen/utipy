
from contextlib import contextmanager
from typing import Callable, Union

from .timestamps import Timestamps

# TODO Add tests


class StepTimer(Timestamps):

    def __init__(self, message: str = "Took:", verbose: bool = True, msg_fn: Callable = print) -> None:
        """
        A `StepTimer` can be used in `with` statements
        to time steps of code and print the execution time.
        All timestamps are kept, why we can get the 
        total time in the end as well.

        See `Timestamps` for methods that can be applied to recorded timestamps.

        Parameters
        ----------
        message : str
            Default message to prefix time with.
            Can be overridden for separate timings with the `message` 
            argument in `.time_step()`.
        verbose : bool
            Whether to print/log/.. the time a step took when using `.time_step()`.
        msg_fn : callable
            The function to use for printing/logging the message.
            E.g. `print` or `logging.info`.
        """
        super().__init__()
        self.message = message
        self.verbose = verbose
        self.msg_fn = msg_fn

    @contextmanager
    def time_step(self, indent: int = 4, message: Union[str, None] = None, name_prefix=None) -> None:
        """
        Function to use in `with` statement. E.g.:

          > timer = StepTimer()
          > with timer.time_step():
          >     a = 2
          >     b = a * 4
          output: 'Took: 00:00:01'

        Parameters
        ----------
        indent : int
            How many spaces to indent message.
        message : str or None
            Step-specific prefix to the time string. 
            When `None`, the message supplied during 
            inialization is used.
        name_prefix : str or None
            Prefix to record special timestamp with.
                The initial timestamp will be recorded with the name `name_prefix + '_start'`.
                The final timestamp will be recorded with the name `name_prefix + '_end'`.
            This allows easily getting the specific timepoints with `.get_stamp()` or 
            the difference between two stamps with `.took()`.

        Yields
        ------
        `None` once.

        Prints
        ------
        When `self.verbose` is `True`, 
            prints message + formatted time.
        """
        try:
            if name_prefix:
                self.special_stamp(name=name_prefix + "_start")
            else:
                self.stamp()
            yield None
        finally:
            if name_prefix:
                self.special_stamp(name=name_prefix + "_end")
            else:
                self.stamp()
            mess = self.message if message is None else message
            if self.verbose:
                self._print_runtime(
                    indent=indent,
                    message=mess
                )

    def _print_runtime(self, indent: int, message: str) -> None:
        """
        Prints the indented message and step time.
        """
        indent_str = "".join([" " for _ in range(indent)])
        self.msg_fn(f"{indent_str}{message} {self.took()}")
