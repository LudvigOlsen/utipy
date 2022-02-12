
import pathlib


def mk_dir(path, arg_name='out_path', verbose=True):
    path = pathlib.Path(path)
    if verbose and not path.exists():
        print(
            f"`{arg_name}` directory does not exist and will be created: {path.resolve()}")
    path.mkdir(parents=True, exist_ok=True)
