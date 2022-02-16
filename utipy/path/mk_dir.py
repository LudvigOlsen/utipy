
import pathlib
from typing import Callable, Union

from utipy.utils.messenger import Messenger


def mk_dir(path: Union[str, pathlib.Path], arg_name: Union[str, None] = 'out_path',
           verbose: bool = True, indent: int = 0, msg_fn: Callable = print):
    """
    Make directory if it doesn't exist.

    Parameters
    ----------
    path : str or `pathlib.Path`
        Path to directory to make.
    arg_name : str or None
        Name of path argument/variable for message 
        when creating a folder and `verbose` is `True`.
    verbose : bool
        Whether to print/log/... a message when creating a folder.
    indent : int
        How much to indent messages.
    msg_fn : callable
        The function to use for printing/logging the message.
        E.g. `print` or `logging.info`.
    """
    path = pathlib.Path(path)
    if verbose and not path.exists():
        if arg_name is None or not arg_name:
            arg_name = ""
        else:
            arg_name = f"`{arg_name}` "
        messenger = Messenger(verbose=verbose, indent=indent, msg_fn=msg_fn)
        messenger(
            f"{arg_name}directory does not exist and will be created: "
            f"{path.resolve()}"
        )
    path.mkdir(parents=True, exist_ok=True)
