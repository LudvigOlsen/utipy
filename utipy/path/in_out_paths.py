
import os
import pathlib
from typing import Callable, List, Optional, Union

from utipy.path.mk_rm_dir import mk_dir, rm_dir as remove_dir
from utipy.path.prepare_paths import prepare_in_out_paths
from utipy.utils.messenger import Messenger


# TODO Add tests
# TODO Allow keys to have a list of paths?

class InOutPaths:

    COLLECTION_NAMES = [
        "in_files",
        "in_dirs",
        "out_files",
        "out_dirs",
        "tmp_files",
        "tmp_dirs"
    ]

    def __init__(self,
                 in_files: dict = None,
                 in_dirs: dict = None,
                 out_files: dict = None,
                 out_dirs: dict = None,
                 tmp_files: dict = None,
                 tmp_dirs: dict = None,
                 allow_none: bool = False,
                 allow_overwriting: bool = True,
                 allow_duplicates_in: List[str] = [
                     "in_dirs", "out_dirs", "tmp_dirs"],
                 disallowed_nestings: List[tuple] = [
                     ("in_files", "tmp_dirs"),
                     ("out_files", "tmp_dirs"),
                     ("in_dirs", "tmp_dirs"),
                     ("out_dirs", "tmp_dirs")
                 ],
                 print_note: bool = "",
                 ) -> None:
        """
        Collection of path collections for keeping track of in- and output paths,
        be it files or directories. Has relevant checks, such as duplication and
        existence, and allows printing a summary of the paths. Paths are converted to 
        `pathlib.Path` objects and missing directories can be created.

        Note: Even when `allow_overwriting` is enabled, 
        `in_files` and `out_files` cannot contain the same paths.

        Keys must be unique across the path dictionaries.

        Parameters
        ----------
        in_files : dict
            Dict with named paths to input files, mapping `(argument) name -> input filepath`.
            A path can also be "-" when streaming input. 
            This value will remain a string and will not be checked
            for duplication, existence, etc.
        in_dirs : dict
            Dict with named paths to input directories, mapping `(argument) name -> input directory path`.
        out_files : dict
            Dict with named paths to output files, mapping `(argument) name -> output filepath`.
        out_dirs : dict
            Dict with named paths to output directories, mapping `(argument) name -> output directory path`.
        tmp_files : dict
            Dict with named paths to temporary files, mapping `(argument) name -> temporary filepath`.
        tmp_dirs : dict
            Dict with named paths to temporary directories, mapping `(argument) name -> temporary directory path`.
        allow_none : bool
            Whether to allow paths (i.e. dict values) to be `None`,
            in which case they will be ignored.
        allow_overwriting : bool
            Whether to allow `out_files` paths to already exist.
        allow_duplicates_in : list
            List of collections to allow duplicate paths in. One of:
                {'in_files', 'in_dirs', 'out_files', 'out_dirs', 'tmp_files', 'tmp_dirs'}.
        disallowed_nestings : list of tuples
            Pairs of collections where the paths of the first cannot 
            be nested inside the paths of the second.
            By default, the in and out paths cannot be located within 
            the temporary directories, as these might be deleted.
        print_note : string
            String to add to end of `__str__` method.
            That is a suffix added when printing the collection.

        Examples
        --------

        Uncomment code to run.

        # # Usually the paths come from input arguments or variables
        # # Additional paths can be added later with `set_path()`.

        # # Initialize the collection of path collections
        # paths = InOutPaths(
        #     in_files={
        #         "in_file": "../dir1/dir2/john.csv",
        #         "stream_in": "-"
        #     },
        #     in_dirs={
        #         "in_dir": "../dir1/dir2/",
        #     },
        #     out_files={
        #         "out_file": "../dir1/dir2/output/no_john.csv"
        #     },
        #     out_dirs={
        #         "out_path": "../dir1/dir2/output/"
        #     }
        # )

        # # Add additional path
        # # Reruns checks to ensure consistency
        # paths.set_path(
        #     name="in_file_2",
        #     path="../dir1/dir2/dennis.csv",
        #     collection="in_files"
        # )
        # # Or set multiple at a time to avoid rerunning checks unnecessarily
        # paths.set_paths(
        #     paths={
        #         "out_file_2": "../dir1/dir2/output/no_dennis.csv"
        #         "out_file_3": "../dir1/dir2/output/readme.txt"
        #     }, 
        #     collection="out_files"
        # )

        # # Create the output directories that do not exist
        # paths.mk_output_dirs(collection="out_dirs")

        # # Get a path
        # paths["in_file"] # or
        # paths.get_path(name="in_file", as_str=False, raise_on_fail=True)

        # # Remove file from disk
        # paths.rm_file(name="in_file")

        # # Update collection with another `InOutPaths` collection
        # # The sub collections are dicts, why this is just dict.update() 
        # # on each sub collection
        # paths.update(other=other_paths)

        # # Find the combinations of keys and paths in the collections of this object
        # # that are not in the collections of another object.
        # paths.difference(other=other_paths):
        """
        self.all_paths = None
        self._collections = {
            "in_files": in_files,
            "in_dirs": in_dirs,
            "out_files": out_files,
            "out_dirs": out_dirs,
            "tmp_files": tmp_files,
            "tmp_dirs": tmp_dirs,
        }

        self.allow_none = allow_none
        self.allow_overwriting = allow_overwriting
        self.allow_duplicates_in = allow_duplicates_in
        self.disallowed_nestings = disallowed_nestings
        self.print_note = print_note

        self._prepare_paths()

    # Properties

    @property
    def npaths(self):
        """
        Total number of stored paths.

        Returns
        -------
        Int
        """
        return sum(self.collection_sizes().values())

    @property
    def collection_sizes(self):
        """
        Sizes of collections (size: number of paths).

        Returns
        -------
        Dict mapping collection name -> number of paths.
        """
        return {
            coll: self.get_collection_size(coll)
            for coll in InOutPaths.COLLECTION_NAMES
        }

    def get_collection_size(self, name: str):
        """
        Get size (number of paths) of a given collection.

        Parameters
        ----------
        name : str
            Name of collection to get size of.

        Returns
        -------
        Int
        """
        coll = self.get_collection(name)
        if coll is None:
            return 0
        return len(coll)

    # Getters and setters

    def get_collection(self, name: str):
        """
        Get collection of paths.

        Parameters
        ----------
        name : str
            Name of collection to get.

        Returns
        -------
        Dict mapping `name -> path`.
        """
        assert isinstance(name, str)
        self._check_collection_name(name)
        return self._collections[name]

    def set_collection(self, name: str, collection: dict):
        """
        Set collection of paths.

        See also: `update()`.

        Parameters
        ----------
        name : str
            Name of collection to set.
        collection : dict 
            Collection of paths as dict, mapping `name -> path`. 
            Replaces existing dict.
        """
        # NOTE: Avoid internal use
        # as it may cause an infinite loop with
        # `self._prepare_paths()`
        self._set_collection(name=name, coll=collection)
        # Ensure consistency
        self._prepare_paths()

    def _set_collection(self, name: str, coll: Union[dict, None]):
        assert isinstance(name, str)
        assert coll is None or isinstance(coll, dict)
        if name not in InOutPaths.COLLECTION_NAMES:
            raise ValueError(
                f"`name` was not one of the allowed collection names: {InOutPaths.COLLECTION_NAMES}")
        self._collections[name] = coll

    def _update_collection(self, paths: dict, collection: str):
        assert isinstance(paths, dict)
        assert isinstance(collection, str)
        self._check_collection_name(collection)
        if self._collections[collection] is None:
            self._set_collection(name=collection, coll=paths)
        self._collections[collection].update(paths)

    def __getitem__(self, name: str):
        """
        Get path from its key:

        e.g. d['key']
        """
        return self.get_path(name=name)

    def get_path(self, name: str, as_str: bool = False, raise_on_fail: bool = True):
        """
        Get a path.

        Parameters
        ----------
        name : str
            Name of path to get.
        as_str : bool
            Whether to convert the path to string (default is as `pathlib.Path`).
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
            When `False`, it defaults to `None`.

        Returns
        -------
        `pathlib.Path`, str or `None`
        """
        if name in self.all_paths:
            return self._format_path_out(path=self.all_paths[name], as_str=as_str)
        if raise_on_fail:
            raise ValueError(
                f"{name} was not a known key in any of the path collections.")
        return None

    def set_path(self, name: str, path: Union[str, pathlib.Path], collection: str):
        """
        Set a path in a collection.

        Parameters
        ----------
        name : str
            Name of path for collection dict.
        path : str or `pathlib.Path` 
            The path to set.
        collection : str
            Name of collection to set the path in.
            When a name already exist it is overwritten.
        """
        # NOTE: Avoid internal use
        # as it may cause an infinite loop
        assert isinstance(name, str)
        assert isinstance(path, (str, pathlib.PurePath))
        self._update_collection(
            paths={name: path}, collection=collection)

        # Ensure consistency
        self._prepare_paths()

    def set_paths(self, paths: dict, collection: str):
        """
        Set one or more paths in a collection.

        Parameters
        ----------
        paths : dict
            Dict mapping `path name -> path`.
            Paths can be of type str or `pathlib.Path`.
        collection : str
            Name of collection to set the path in.
        """
        # NOTE: Avoid internal use
        # as it may cause an infinite loop
        self._update_collection(paths=paths, collection=collection)

        # Ensure consistency
        self._prepare_paths()

    # Handle paths

    def check_paths(self):
        """
        Call path checks manually. 

        These checks are automatically called after each mutation with 
        setter methods, but when overwriting attributes (like check settings) 
        manually, we may need to call it externally.
        """
        self._prepare_paths()

    def _prepare_paths(self):
        # Prepare paths
        self._collections, self.all_paths = prepare_in_out_paths(
            named_collections=self._collections,
            allow_none=self.allow_none,
            allow_overwriting=self.allow_overwriting,
            allow_duplicates_in=self.allow_duplicates_in,
            disallowed_nestings=self.disallowed_nestings,
            pathlib_out=True)

    def mk_output_dir(
        self,
        name: str,
        messenger: Optional[Callable] = Messenger(
            verbose=True, indent=0, msg_fn=print)
    ):
        """
        Create non-existing output directory for a given path.

        For filepaths, it creates the directory the file is located in.

        Parameters
        ----------
        name : str
            Name of path to create output directory for.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g. `print`)
            and potential indentation.
        """
        path = self.get_path(name=name)
        dir_path = pathlib.Path(path).parent
        mk_dir(
            path=dir_path,
            arg_name=name,
            messenger=messenger
        )

    def mk_output_dirs(
        self,
        collection: str = None,
        messenger: Optional[Callable] = Messenger(
            verbose=True, indent=0, msg_fn=print)
    ):
        """
        Create non-existing output directories.

        For filepaths, it creates the directory the file is located in.

        Parameters
        ----------
        collection : str
            Name of collection to create output directories for.
                One of: ('out_dirs', 'out_files', 'tmp_files', 'mkdirs_for_tmp_dirs')
            When `None`, directories are created for all three collections.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g. `print`)
            and potential indentation.
        """

        # Find which collections to create output dirs for
        mkdirs_for_out_files = True
        mkdirs_for_out_dirs = True
        mkdirs_for_tmp_files = True
        mkdirs_for_tmp_dirs = True
        if collection is not None:
            if collection not in ["out_files", "out_dirs", "tmp_files", "tmp_dirs"]:
                raise ValueError(
                    f"`collection` must be one of the output path collections but was {collection}.")
            if collection != "out_files":
                mkdirs_for_out_files = False
            if collection != "out_dirs":
                mkdirs_for_out_files = False
            if collection != "tmp_files":
                mkdirs_for_tmp_files = False
            if collection != "tmp_dirs":
                mkdirs_for_tmp_dirs = False

        # Create output directories if they don't exist

        # For output directories
        if mkdirs_for_out_dirs:
            out_dirs = self.get_collection("out_dirs")
            if out_dirs is None:
                raise ValueError("`out_dirs` collection was `None`.")
            for k, v in out_dirs.items():
                mk_dir(path=v, arg_name=k, messenger=messenger)

        # For output files' directories
        if mkdirs_for_out_files:
            out_files = self.get_collection("out_files")
            if out_files is None:
                raise ValueError("`out_files` collection was `None`.")
            for k, v in out_files.items():
                # Get directory the file should be place in
                dir_path = pathlib.Path(v).parent
                mk_dir(path=dir_path, arg_name=k, messenger=messenger)

        # For tmp directories
        if mkdirs_for_tmp_dirs:
            tmp_dirs = self.get_collection("tmp_dirs")
            if tmp_dirs is None:
                raise ValueError("`tmp_dirs` collection was `None`.")
            for k, v in tmp_dirs.items():
                mk_dir(path=v, arg_name=k, messenger=messenger)

        # For tmp files' directories
        if mkdirs_for_tmp_files:
            tmp_files = self.get_collection("tmp_files")
            if tmp_files is None:
                raise ValueError("`tmp_files` collection was `None`.")
            for k, v in tmp_files.items():
                # Get directory the file should be place in
                dir_path = pathlib.Path(v).parent
                mk_dir(path=dir_path, arg_name=k, messenger=messenger)

    def rm_file(self, name: str, raise_on_fail: bool = True):
        """
        Remove a file from disk.

        Parameters
        ----------
        name : str
            Name of path to a file to remove from disk.
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
        """
        path = self[name]
        if path is None:
            raise ValueError(f"Path object for `{name}` was `None`.")
        if not path.is_file():
            if raise_on_fail:
                raise RuntimeError(
                    f"Path for `{name}` was not an existing file: {path}")
        else:
            os.remove(str(path))

    def rm_dir(self, name: str, raise_on_fail: bool = True,
               messenger: Optional[Callable] = Messenger(
                   verbose=True, indent=0, msg_fn=print)) -> None:
        """
        Remove a directory from disk.

        Parameters
        ----------
        name : str
            Name of path to a directory to remove from disk.
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g. `print`)
            and potential indentation.
        """
        path = self[name]
        if path is None:
            raise ValueError(f"Path object for `{name}` was `None`.")
        remove_dir(
            path=path,
            arg_name=f'{name} path',
            raise_missing=raise_on_fail,
            raise_not_dir=raise_on_fail,
            messenger=messenger
        )

    def rm_tmp_dirs(self, raise_on_fail: bool = True,
                    messenger: Optional[Callable] = Messenger(
                        verbose=True, indent=0, msg_fn=print)) -> None:
        """
        Remove all temporary directories from disk.

        Parameters
        ----------
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g. `print`)
            and potential indentation.
        """

        # TODO In case they are nested, we should check their existence
        # before deleting some of the directories, as that might
        # delete the existing ones

        # Delete each path in `tmp_dirs``
        for path in self.get_collection(name="tmp_dirs").keys():
            self.rm_dir(
                name=path,
                raise_on_fail=raise_on_fail,
                messenger=messenger
            )

    def update(self, other: object):
        """
        Update with paths from another `InOutPaths` collection.

        Parameters
        ----------
        other : `InOutPaths` instance
            Another `InOutPaths` instance with paths.
            Each sub collection is dict-updated one at a time.
        """
        assert isinstance(other, InOutPaths)
        for coll_name in InOutPaths.COLLECTION_NAMES:
            self._update_collection(
                paths=other.get_collection(name=coll_name),
                collection=coll_name
            )

        # Ensure consistency
        self._prepare_paths()

    def difference(self, other: object):
        """
        Find the combinations of keys and paths in the collections of this object
        that are not in the collections of the `other` object.
        Creates a new `InOutPaths` object with the settings from this object.

        Parameters
        ----------
        other : `InOutPaths` instance
            Another `InOutPaths` instance with paths.
            Each sub collection is dict-updated one at a time.

        Returns
        -------
        `InOutPaths` instance
            A new `InOutPaths` instance with the keys and paths in 
            the collections of this object that are not in the collections 
            of the `other` object.
        """
        assert isinstance(other, InOutPaths)
        diff_dicts = {}
        for coll_name in InOutPaths.COLLECTION_NAMES:
            this_coll = self.get_collection(name=coll_name)
            if this_coll is None:
                diff_dicts[coll_name] = None
                continue
            other_coll = other.get_collection(name=coll_name)
            if other_coll is None:
                diff_dicts[coll_name] = this_coll
                continue
            this_coll = set(this_coll.items())
            other_coll = set(other_coll.items())
            diff_dicts[coll_name] = dict(this_coll.difference(other_coll))
        return self._new(
            in_files=diff_dicts["in_files"],
            in_dirs=diff_dicts["in_dirs"],
            out_files=diff_dicts["out_files"],
            out_dirs=diff_dicts["out_dirs"],
            tmp_files=diff_dicts["tmp_files"],
            tmp_dirs=diff_dicts["tmp_dirs"],
        )

    def __eq__(self, other: object) -> bool:
        """
        Check equality of this `InOutPaths` instance and another.

        Checks that all sub collections are the same. 
        No other attributes are considered.

        Parameters
        ----------
        other : `InOutPaths` instance
            Another `InOutPaths` instance with paths.
        """
        assert isinstance(other, InOutPaths)
        if self.npaths != other.npaths:
            return False
        for coll_name in InOutPaths.COLLECTION_NAMES:
            this_coll = self.get_collection(name=coll_name)
            other_coll = other.get_collection(name=coll_name)
            if sum([other_coll is None, this_coll is None]) == 1:
                return False
            if this_coll != other_coll:
                return False
        return True

    def _new(self, in_files: dict = None, in_dirs: dict = None, out_files: dict = None, out_dirs: dict = None, tmp_files: dict = None, tmp_dirs: dict = None):
        """
        Create new `InOutPaths` object with new collections but keeping the rest of the settings.

        Parameters
        ----------
        in_files : dict
            Dict with named paths to input files, mapping `(argument) name -> input filepath`.
            A path can also be "-" when streaming input. 
            This value will remain a string and will not be checked
            for duplication, existence, etc.
        in_dirs : dict
            Dict with named paths to input directories, mapping `(argument) name -> input directory path`.
        out_files : dict
            Dict with named paths to output files, mapping `(argument) name -> output filepath`.
        out_dirs : dict
            Dict with named paths to output directories, mapping `(argument) name -> output directory path`.
        tmp_files : dict
            Dict with named paths to temporary files, mapping `(argument) name -> temporary filepath`.
        tmp_dirs : dict
            Dict with named paths to temporary directories, mapping `(argument) name -> temporary directory path`.

        Returns
        -------
        `InOutPaths` instance
        """
        return InOutPaths(
            in_files=in_files,
            in_dirs=in_dirs,
            out_files=out_files,
            out_dirs=out_dirs,
            tmp_files=tmp_files,
            tmp_dirs=tmp_dirs,
            allow_none=self.allow_none,
            allow_overwriting=self.allow_overwriting,
            allow_duplicates_in=self.allow_duplicates_in,
            print_note=self.print_note
        )

    def _check_collection_name(self, name: str):
        if name not in InOutPaths.COLLECTION_NAMES:
            raise ValueError(f"Collection name was unknown: {name}.")

    def _format_path_out(self, path, as_str: bool):
        if as_str:
            path = str(path)
        return path

    def __str__(self) -> str:
        """
        Convert object to a string with the paths for each sub collection.
        """
        max_paths_per_coll = 10
        lines = []
        lines.append("Input and output paths")
        for coll_name in InOutPaths.COLLECTION_NAMES:
            collection = self.get_collection(name=coll_name)
            if collection is None:
                lines.append(f"  {coll_name} (0)")
            else:
                lines.append(f"  {coll_name} ({len(collection)}):")
                sorted_keys = sorted(collection.keys())
                for i, key in enumerate(sorted_keys):
                    if i < max_paths_per_coll:
                        lines.append(f"    {key} -> {collection[key]}")
                    else:
                        lines.append(f"    ...")
                        break
        if self.print_note:
            lines.append(f"  Note: {self.print_note}")
        return "\n".join(lines)
