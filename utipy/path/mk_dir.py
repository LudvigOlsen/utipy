
import pathlib
from typing import Union

# TODO Convert to logging, so it can be turned off when not debugging


def mk_dir(path: Union[str, pathlib.Path], arg_name: Union[str, None] = 'out_path', verbose: bool = True):
    """
    Make directory if it doesn't exist.

    Parameters
    ----------
    path : str or `pathlib.Path`
        Path to directory to make.
    arg_name : str or None
        Name of path argument/variable for message 
        when creating a folder and `verbose` is `True`.
    verbose: bool
        Whether to print a message when creating a folder.
    """
    path = pathlib.Path(path)
    if verbose and not path.exists():
        if arg_name is None or not arg_name:
            arg_name = ""
        else:
            arg_name = f"`{arg_name}` "
        print(
            f"{arg_name}directory does not exist and will be created: "
            f"{path.resolve()}")
    path.mkdir(parents=True, exist_ok=True)
