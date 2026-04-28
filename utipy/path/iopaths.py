import os
import pathlib
from typing import Callable, Dict, List, Optional, Union
from typing import Literal, overload

from utipy.path.mk_rm_dir import mk_dir, rm_dir as remove_dir
from utipy.path.prepare_paths import prepare_in_out_paths
from utipy.utils.messenger import Messenger


# TODO Add tests
# TODO Allow keys to have a list of paths?
# TODO Allow checking if dirs are empty (e.g., checkpoints)


def default_allow_duplicates_in():
    return ["in_dirs", "out_dirs", "tmp_dirs"]


def default_disallowed_nestings():
    return [
        ("in_files", "tmp_dirs"),
        ("out_files", "tmp_dirs"),
        ("in_dirs", "tmp_dirs"),
        ("out_dirs", "tmp_dirs"),
    ]


class IOPaths:
    COLLECTION_NAMES = [
        "in_files",
        "in_dirs",
        "out_files",
        "out_dirs",
        "tmp_files",
        "tmp_dirs",
    ]

    def __init__(
        self,
        in_files: Optional[Dict[str, Union[str, pathlib.PurePath]]] = None,
        in_dirs: Optional[Dict[str, Union[str, pathlib.PurePath]]] = None,
        out_files: Optional[Dict[str, Union[str, pathlib.PurePath]]] = None,
        out_dirs: Optional[Dict[str, Union[str, pathlib.PurePath]]] = None,
        tmp_files: Optional[Dict[str, Union[str, pathlib.PurePath]]] = None,
        tmp_dirs: Optional[Dict[str, Union[str, pathlib.PurePath]]] = None,
        allow_none: bool = False,
        allow_overwriting: bool = True,
        allow_duplicates_in: Optional[List[str]] = None,
        disallowed_nestings: Optional[List[tuple]] = None,
        print_note: str = "",
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
            Defaults to 'in_dirs', 'out_dirs', and 'tmp_dirs'.
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

        Initialize the collection of path collections.
        Usually the paths come from input arguments or variables.
        Additional paths can be added later with `set_path()`.

        >>> paths = IOPaths(
        ...     in_files={
        ...         "in_file": "../dir1/dir2/john.csv",
        ...         "stream_in": "-"
        ...     },
        ...     in_dirs={
        ...         "in_dir": "../dir1/dir2/",
        ...     },
        ...     out_files={
        ...         "out_file": "../dir1/dir2/output/no_john.csv"
        ...     },
        ...     out_dirs={
        ...         "out_path": "../dir1/dir2/output/"
        ...     }
        ... )

        Add additional path. Reruns checks to ensure consistency.

        >>> paths.set_path(
        ...     name="in_file_2",
        ...     path="../dir1/dir2/dennis.csv",
        ...     collection="in_files"
        ... )

        Or set multiple at a time to avoid rerunning checks unnecessarily.

        >>> paths.set_paths(
        ...     paths={
        ...         "out_file_2": "../dir1/dir2/output/no_dennis.csv"
        ...         "out_file_3": "../dir1/dir2/output/readme.txt"
        ...     },
        ...     collection="out_files"
        ... )

        Create the output directories that do not exist.

        >>> paths.mk_output_dirs(collection="out_dirs")

        Get a path.

        >>> paths["in_file"]  # or
        >>> paths.get_path(name="in_file", as_str=False, raise_on_fail=True)

        Remove file from disk.

        >>> paths.rm_file(name="in_file")

        Update collection with another `IOPaths` collection.
        The sub collections are dicts, why this is just dict.update()
        on each sub collection.

        >>> paths.update(other=other_paths)

        Find the combinations of keys and paths in the collections of this object
        that are not in the collections of another object.

        >>> paths.difference(other=other_paths):
        """
        # Set defaults for mutable types
        if allow_duplicates_in is None:
            allow_duplicates_in = default_allow_duplicates_in()
        if disallowed_nestings is None:
            disallowed_nestings = default_disallowed_nestings()

        self.all_paths: Dict[str, Union[pathlib.Path, str]] = {}
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
        return sum(self.collection_sizes.values())

    @property
    def collection_sizes(self):
        """
        Sizes of collections (size: number of paths).

        Returns
        -------
        Dict mapping collection name -> number of paths.
        """
        return {
            coll: self.get_collection_size(coll) for coll in IOPaths.COLLECTION_NAMES
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
        if not isinstance(name, str):
            raise TypeError("`name` must be a string.")
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
        if not isinstance(name, str):
            raise TypeError("`name` must be a string.")
        if coll is not None and not isinstance(coll, dict):
            raise TypeError("`coll` must be either a dict or `None`.")
        if name not in IOPaths.COLLECTION_NAMES:
            raise ValueError(
                f"`name` was not one of the allowed collection names: {IOPaths.COLLECTION_NAMES}"
            )
        self._collections[name] = coll

    def _update_collection(self, paths: dict, collection: str):
        if not isinstance(paths, dict):
            raise TypeError("`paths` must be a dict.")
        if not isinstance(collection, str):
            raise TypeError("`collection` must be a string.")
        self._check_collection_name(collection)

        coll = self._collections[collection]
        if coll is None:
            self._set_collection(name=collection, coll=paths)
            return
        coll.update(paths)

    def __getitem__(self, name: str) -> Union[pathlib.Path, str]:
        """
        Get path from its key:

        E.g., `d['key']`

        Usually returns `pathlib.Path`. May return '-' for stream paths.
        """
        path = self.get_path(name=name)
        if path is None:
            raise RuntimeError(
                f"Internal error: `{name}` was found but resolved to `None`."
            )
        return path

    def get_path(
        self, name: str, as_str: bool = False, raise_on_fail: bool = True
    ) -> Optional[Union[pathlib.Path, str]]:
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
                f"{name} was not a known key in any of the path collections."
            )
        return None

    def set_path(
        self, name: str, path: Union[str, pathlib.PurePath], collection: str
    ) -> None:
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
        if not isinstance(name, str):
            raise TypeError("`name` must be a string.")
        if not isinstance(path, (str, pathlib.PurePath)):
            raise TypeError("`path` must be a string or pathlib path.")
        self._update_collection(paths={name: path}, collection=collection)

        # Ensure consistency
        self._prepare_paths()

    def set_paths(self, paths: dict, collection: str) -> None:
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

    def rm_path(self, name: str) -> None:
        """
        Remove path from collection.

        Parameters
        ----------
        name : str
            Name of path in collection.
        """
        coll_name = self.get_collection_name_by_path_name(name)
        coll = self._collections[coll_name]
        if coll is None:
            raise RuntimeError(
                f"Internal error: `{name}` was found in collection `{coll_name}`, "
                "but the collection was `None`."
            )
        del coll[name]
        del self.all_paths[name]

    def rm_paths(self, names: List[str]) -> None:
        """
        Remove paths from collections.

        Parameters
        ----------
        names : list of str
            Names of paths in one or more collections.
        """
        [self.rm_path(name=name) for name in names]

    def rm_paths_in_dir(
        self,
        dir_path_name: Optional[str] = None,
        dir_path: Optional[Union[str, pathlib.PurePath]] = None,
        rm_dir_path: bool = True,
    ) -> None:
        """
        Remove paths from collection that are within a directory.

        Directory can be specified either as the name of a path in the collections
        or a new path. The directory does not need to exist.

        Parameters
        ----------
        dir_path_name : str or `None`
            Name of path in the collections.
        dir_path : str or `pathlib.Path` or `None`
            A path to a directory.
            No checks are done on this path but it is
            resolved with `pathlib.Path.resolve()`.
        rm_dir_path : bool
            Whether to remove the path to the directory itself.
        """
        if sum([dir_path_name is not None, dir_path is not None]) != 1:
            raise ValueError(
                "Exactly one of {`dir_path_name`, `dir_path`} should be specified."
            )
        if dir_path_name is not None:
            dir_path = self[dir_path_name]
        if dir_path is None:
            raise RuntimeError("Internal error: directory path resolved to `None`.")
        if str(dir_path) == "-":
            raise ValueError("`-` is a stream path, not a directory path.")

        dir_path = pathlib.Path(dir_path).resolve()

        path_names_to_remove = []
        for path_key, path_val in self.all_paths.items():
            if str(path_val) == "-":
                continue

            resolved_path = pathlib.Path(path_val).resolve()
            is_dir_path = resolved_path == dir_path
            is_in_dir = dir_path in resolved_path.parents

            if is_in_dir or (rm_dir_path and is_dir_path):
                path_names_to_remove.append(path_key)
        self.rm_paths(names=path_names_to_remove)

    def get_collection_name_by_path_name(self, name: str) -> str:
        """
        Get name of the collection a path is in.

        Parameters
        ----------
        name : str
            Name of path.

        Returns
        -------
        str
            Name of collection containing the path name.
        """
        if name not in self.all_paths:
            raise ValueError("`name` was not in any of the collections.")
        for coll_name, coll_paths_dict in self._collections.items():
            if coll_paths_dict is not None and name in coll_paths_dict:
                return coll_name
        raise RuntimeError(
            f"Internal error: `{name}` was in `all_paths` but not in any collection."
        )

    # Handle paths

    def check_paths(self):
        """
        Call path checks manually.

        These checks are automatically called after each mutation with
        setter methods, but when overwriting attributes (like check settings)
        manually, we may need to call it externally.

        May be meaningful to run after removing files and paths, as this
        does not rerun the checks.
        """
        # TODO Add better description of the checks
        self._prepare_paths()

    def _prepare_paths(self):
        # Prepare paths
        self._collections, self.all_paths = prepare_in_out_paths(
            named_collections=self._collections,
            allow_none=self.allow_none,
            allow_overwriting=self.allow_overwriting,
            allow_duplicates_in=self.allow_duplicates_in,
            disallowed_nestings=self.disallowed_nestings,
            pathlib_out=True,
            copy=True,
        )

    def mk_output_dir(
        self,
        name: str,
        messenger: Optional[Callable] = Messenger(verbose=True, indent=0, msg_fn=print),
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
            The messenger determines the messaging function (e.g., `print`)
            and potential indentation.
        """
        path = self.get_path(name=name, raise_on_fail=True)
        if path is None:
            raise RuntimeError(
                f"Internal error: `{name}` was found but resolved to `None`."
            )
        if str(path) == "-":
            raise ValueError(
                f"`{name}` is a stream input path (`-`) and "
                "has no output directory to create."
            )

        dir_path = pathlib.Path(path).parent
        mk_dir(path=dir_path, arg_name=name, messenger=messenger)

    def mk_output_dirs(
        self,
        collection: Optional[str] = None,
        messenger: Optional[Callable] = Messenger(verbose=True, indent=0, msg_fn=print),
    ):
        """
        Create non-existing output directories.

        For filepaths, it creates the directory the file is located in.

        Parameters
        ----------
        collection : str
            Name of collection to create output directories for.
                One of: ('out_dirs', 'out_files', 'tmp_files', 'tmp_dirs')
            When `None`, directories are created for all four collections.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g., `print`)
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
                    f"`collection` must be one of the output path collections but was {collection}."
                )
            if collection != "out_files":
                mkdirs_for_out_files = False
            if collection != "out_dirs":
                mkdirs_for_out_dirs = False
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

    def rm_file(self, name: str, rm_path: bool = True, raise_on_fail: bool = True):
        """
        Remove a file from disk.

        Parameters
        ----------
        name : str
            Name of path to a file to remove from disk.
        rm_path : bool
            Whether to remove path from path collection.
            NOTE: For files that need to exist (e.g., those in the `in_files` collection),
            leaving the path after removing the file will cause downstream
            checking of the paths (see `.check_paths()`) will fail
            (as we removed the files). Those checks are called as part of
            some of the methods.
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
        """
        path = self[name]
        if path is None:
            raise ValueError(f"Path object for `{name}` was `None`.")
        if str(path) == "-":
            raise ValueError(
                f"`{name}` is a stream input path (`-`) and cannot be removed."
            )

        if not pathlib.Path(path).is_file():
            if raise_on_fail:
                raise RuntimeError(
                    f"Path for `{name}` was not an existing file: {path}"
                )
        else:
            os.remove(str(path))

        if rm_path:
            self.rm_path(name=name)

    def rm_dir(
        self,
        name: str,
        rm_paths: bool = True,
        raise_on_fail: bool = True,
        messenger: Optional[Callable] = Messenger(verbose=True, indent=0, msg_fn=print),
    ) -> None:
        """
        Remove a directory from disk.

        Parameters
        ----------
        name : str
            Name of path to a directory to remove from disk.
        rm_paths : bool
            Whether to remove all paths that are within the
            removed directory as well as the path to the
            directory itself.
            NOTE: For files that need to exist (e.g., those in the `in_files` collection),
            leaving the path after removing the file will cause downstream
            checking of the paths (see `.check_paths()`) will fail
            (as we removed the files). Those checks are called as part of
            some of the methods.
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g., `print`)
            and potential indentation.
        """
        path = self[name]
        if path is None:
            raise ValueError(f"Path object for `{name}` was `None`.")
        if str(path) == "-":
            raise ValueError(
                f"`{name}` is a stream input path (`-`) and is not a directory."
            )

        remove_dir(
            path=path,
            arg_name=f"{name} path",
            raise_missing=raise_on_fail,
            raise_not_dir=raise_on_fail,
            messenger=messenger,
        )
        if rm_paths:
            self.rm_paths_in_dir(dir_path=path, rm_dir_path=True)

    def rm_tmp_dirs(
        self,
        rm_paths: bool = True,
        raise_on_fail: bool = True,
        messenger: Optional[Callable] = Messenger(verbose=True, indent=0, msg_fn=print),
    ) -> None:
        """
        Remove all temporary directories from disk.

        Parameters
        ----------
        rm_paths : bool
            Whether to remove all paths that are within the
            removed directories and the paths to the directories
            themselves.
        raise_on_fail : bool
            Whether to raise an error when the path does not exist.
        messenger : `utipy.Messenger` or None
            A `utipy.Messenger` instance used to print/log/... information.
            When `None`, no printing/logging is performed.
            The messenger determines the messaging function (e.g., `print`)
            and potential indentation.
        """

        tmp_dirs = self.get_collection(name="tmp_dirs")
        if tmp_dirs is None:
            raise ValueError("`tmp_dirs` collection was `None`.")

        # Resolve paths once before mutation. The removal step may delete path
        # entries from the collections, so later logic should not depend on
        # iterating over the live `tmp_dirs` dict.
        path_items = [
            (path_key, pathlib.Path(path).resolve())
            for path_key, path in tmp_dirs.items()
        ]

        if raise_on_fail:
            # Check all tmp dirs before removing any of them. This avoids
            # partially deleting directories and then failing on a later path.
            for path_key, path in path_items:
                if not path.exists():
                    raise RuntimeError(f"`{path_key}` path did not exist: {path}")
                if not path.is_dir():
                    raise RuntimeError(f"`{path_key}` path was not a directory: {path}")

        # When tmp dirs are nested, deleting the parent removes the child on
        # disk too. Only remove top-level dirs to avoid raising on a child path
        # that was already deleted as part of its parent.
        seen_top_level_paths = set()
        top_level_path_keys = []
        for path_key, path in path_items:
            if any(
                other_path != path and other_path in path.parents
                for _, other_path in path_items
            ):
                continue
            if path in seen_top_level_paths:
                continue
            seen_top_level_paths.add(path)
            top_level_path_keys.append(path_key)

        # Re-read the live collection for each deletion because `rm_dir()` can
        # remove path entries when `rm_paths=True`.
        for path_key in top_level_path_keys:
            tmp_dirs = self.get_collection(name="tmp_dirs")
            if tmp_dirs is not None and path_key in tmp_dirs:
                self.rm_dir(
                    name=path_key,
                    rm_paths=rm_paths,
                    raise_on_fail=raise_on_fail,
                    messenger=messenger,
                )

    def mv_file(
        self,
        name: str,
        new_path: Union[str, pathlib.PurePath],
        update_path: bool = True,
    ) -> None:
        """
        Move a file to a new path.
        Optionally update the path for `name` in the collection.

        When updating the path after moving the file, it re-checks
        the paths. See `.check_paths()` for details.
        """
        path = self[name]
        if path is None:
            raise ValueError(f"Path object for `{name}` was `None`.")
        if str(path) == "-":
            raise ValueError(
                f"`{name}` is a stream input path (`-`) and cannot be moved."
            )

        path = pathlib.Path(path)
        new_path = pathlib.Path(new_path)
        path.rename(new_path)
        if update_path:
            coll_name = self.get_collection_name_by_path_name(name=name)
            coll = self._collections[coll_name]
            if coll is None:
                raise RuntimeError(
                    f"Internal error: `{name}` was found in collection `{coll_name}`, "
                    "but the collection was `None`."
                )
            coll[name] = new_path
            self._prepare_paths()

    def update(self, other: object):
        """
        Update with paths from another `IOPaths` collection.

        Note: When a collection in `other` is `None`, we
        keep the original collection.

        Parameters
        ----------
        other : `IOPaths` instance
            Another `IOPaths` instance with paths.
            Each sub collection is dict-updated one at a time.
        """
        if not isinstance(other, IOPaths):
            raise TypeError("`other` must be an `IOPaths` instance.")
        for coll_name in IOPaths.COLLECTION_NAMES:
            other_paths = other.get_collection(name=coll_name)
            if other_paths is None:
                continue
            self._update_collection(paths=other_paths, collection=coll_name)

        # Ensure consistency
        self._prepare_paths()

    def difference(self, other: object):
        """
        Find the combinations of keys and paths in the collections of this object
        that are not in the collections of the `other` object.
        Creates a new `IOPaths` object with the settings from this object.

        Parameters
        ----------
        other : `IOPaths` instance
            Another `IOPaths` instance with paths.
            Each sub collection is dict-updated one at a time.

        Returns
        -------
        `IOPaths` instance
            A new `IOPaths` instance with the keys and paths in
            the collections of this object that are not in the collections
            of the `other` object.
        """
        if not isinstance(other, IOPaths):
            raise TypeError("`other` must be an `IOPaths` instance.")
        diff_dicts = {}
        for coll_name in IOPaths.COLLECTION_NAMES:
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
        Check equality of this `IOPaths` instance and another.

        Checks that all sub collections are the same.
        No other attributes are considered.

        Parameters
        ----------
        other : `IOPaths` instance
            Another `IOPaths` instance with paths.
        """
        if not isinstance(other, IOPaths):
            return False
        if self.npaths != other.npaths:
            return False
        for coll_name in IOPaths.COLLECTION_NAMES:
            this_coll = self.get_collection(name=coll_name)
            other_coll = other.get_collection(name=coll_name)
            if sum([other_coll is None, this_coll is None]) == 1:
                return False
            if this_coll != other_coll:
                return False
        return True

    def _new(
        self,
        in_files: Optional[dict] = None,
        in_dirs: Optional[dict] = None,
        out_files: Optional[dict] = None,
        out_dirs: Optional[dict] = None,
        tmp_files: Optional[dict] = None,
        tmp_dirs: Optional[dict] = None,
    ):
        """
        Create new `IOPaths` object with new collections but keeping the rest of the settings.

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
        `IOPaths` instance
        """
        return IOPaths(
            in_files=in_files,
            in_dirs=in_dirs,
            out_files=out_files,
            out_dirs=out_dirs,
            tmp_files=tmp_files,
            tmp_dirs=tmp_dirs,
            allow_none=self.allow_none,
            allow_overwriting=self.allow_overwriting,
            allow_duplicates_in=self.allow_duplicates_in,
            print_note=self.print_note,
        )

    def _check_collection_name(self, name: str):
        if name not in IOPaths.COLLECTION_NAMES:
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
        for coll_name in IOPaths.COLLECTION_NAMES:
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
                        lines.append("    ...")
                        break
        if self.print_note:
            lines.append(f"  Note: {self.print_note}")
        return "\n".join(lines)
