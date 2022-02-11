
from contextlib import contextmanager

from .timestamps import Timestamps


class StepTimer(Timestamps):

    def __init__(self, message="Took:", verbose=True) -> None:
        """
        A `StepTimer` can be used in `with` statements
        to time steps of code and print the execution time.
        All timestamps are kept, why we can get the 
        total time in the end as well.
        """
        super().__init__()
        self.message = message
        self.verbose = verbose

    @contextmanager
    def time_step(self, indent=4, message=None):
        """
        Function to use in `with` statement. E.g.:

          > timer = StepTimer()
          > with timer.time_step():
          >     a = 2
          >     b = a * 4
          output: 'Took: 00:00:01'

        :param indent: How many spaces to indent message.
        :param message: Step-specific prefix to the time string. 
            When `None`, the message supplied during 
            inialization is used.
        :yields: `None` once.
        :returns: `None`.
        :prints: When `self.verbose` is `True`, 
            prints message + formatted time.
        """
        try:
            self.stamp()
            yield None
        finally:
            self.stamp()
            mess = self.message if message is None else message
            if self.verbose:
                self._print_runtime(indent=indent, message=mess)

    def _print_runtime(self, indent, message):
        indent_str = "".join([" " for _ in range(indent)])
        print(f"{indent_str}{message} {self.took()}")
