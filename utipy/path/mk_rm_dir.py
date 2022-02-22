
import pathlib
import shutil
from typing import Callable, Optional, Union

from utipy.utils.messenger import Messenger


def mk_dir(path: Union[str, pathlib.Path], arg_name: Union[str, None] = "",
           raise_on_exists: bool = False, verbose: bool = True, indent: int = 0,
           msg_fn: Callable = print):
    """
    Make directory if it doesn't exist.

    Parameters
    ----------
    path : str or `pathlib.Path`
        Path to directory to make.
    arg_name : str or None
        Name of path argument/variable for message 
        when creating a directory and `verbose` is `True`.
    raise_on_exists : bool
        Whether to raise a RuntimeError when the directory already exists.
    verbose : bool
        Whether to print/log/... a message when creating a directory.
    indent : int
        How much to indent messages.
    msg_fn : callable
        The function to use for printing/logging the message.
        E.g. `print` or `logging.info`.
    """
    path = pathlib.Path(path)
    path_exists = path.exists()

    # Prepare arg name
    arg_name = _prep_arg_name(arg_name)

    # Fail for existing directory (when specified)
    if raise_on_exists and path_exists:
        raise RuntimeError(
            f"{arg_name}directory already exists: {path.resolve()}")

    # Message user about the creation of a new directory
    if verbose and not path_exists:
        messenger = Messenger(verbose=verbose, indent=indent, msg_fn=msg_fn)
        messenger(
            f"{arg_name}directory does not exist and will be created: "
            f"{path.resolve()}"
        )

    # Create new directory if it does not already exist
    path.mkdir(parents=True, exist_ok=True)


def rm_dir(
    path: Union[str, pathlib.Path],
    arg_name: Union[str, None] = "",
    raise_missing: bool = False,
    raise_not_dir: bool = True,
    shutil_ignore_errors: bool = False,
    shutil_onerror: Optional[Callable] = None,
    verbose: bool = True,
    indent: int = 0,
    msg_fn: Callable = print
):
    """
    Remove directory and its contents if it exists using `shutil.rmtree()`.

    Parameters
    ----------
    path : str or `pathlib.Path`
        Path to directory to remove.
    arg_name : str or None
        Name of path argument/variable for message 
        when creating a directory and `verbose` is `True`.
    raise_missing : bool
        Whether to raise a RuntimeError when the directory does not exist.
    raise_not_dir : bool
        Whether to raise a RuntimeError when the path is not to a directory.
    shutil_ignore_errors : bool
        Passed to the `ignore_errors` argument in `shutil.rmtree()`.
    shutil_onerror : bool
        Passed to the `onerror` argument in `shutil.rmtree()`.
    verbose : bool
        Whether to print/log/... a message when creating a directory.
    indent : int
        How much to indent messages.
    msg_fn : callable
        The function to use for printing/logging the message.
        E.g. `print` or `logging.info`.
    """
    path = pathlib.Path(path)
    path_exists = path.exists()

    # Prepare arg name
    arg_name = _prep_arg_name(arg_name)

    if raise_missing and not path_exists:
        raise RuntimeError(f"{arg_name}path did not exist: {path}")

    if path_exists and raise_not_dir and not path.is_dir():
        raise RuntimeError(f"{arg_name}path was not a directory: {path}")

    if path_exists and path.is_dir():
        # Message user about the removal of the directory
        if verbose:
            messenger = Messenger(
                verbose=verbose, indent=indent, msg_fn=msg_fn)
            messenger(
                f"{arg_name}directory will be removed: "
                f"{path.resolve()}"
            )
        shutil.rmtree(path, ignore_errors=shutil_ignore_errors,
                      onerror=shutil_onerror)


def _prep_arg_name(arg_name):

    if arg_name is None or not arg_name:
        arg_name = ""
    else:
        arg_name = f"`{arg_name}` "
    return arg_name
