
import os
import pathlib
from sys import path

from utipy.path.mk_dir import mk_dir
from utipy.path.prepare_paths import prepare_in_out_paths


# TODO Add docs
# TODO Add tests
# TODO Allow keys to have a list of paths?

class InOutPaths:

    COLLECTION_NAMES = [
        "in_files",
        "in_dirs",
        "out_files",
        "out_dirs",
        "tmp_files"
    ]

    def __init__(self,
                 in_files=None,
                 in_dirs=None,
                 out_files=None,
                 out_dirs=None,
                 tmp_files=None,
                 allow_none=False,
                 allow_overwriting=True,
                 allow_duplicates_in_files=False,
                 allow_duplicates_in_dirs=True,
                 allow_duplicates_out_files=False,
                 allow_duplicates_out_dirs=True,
                 allow_duplicates_tmp_files=True,
                 print_note="",
                 ) -> None:

        self.all_paths = None
        self._collections = {
            "in_files": in_files,
            "in_dirs": in_dirs,
            "out_files": out_files,
            "out_dirs": out_dirs,
            "tmp_files": tmp_files,
        }

        self.allow_none = allow_none
        self.allow_overwriting = allow_overwriting
        self.allow_duplicates_in_files = allow_duplicates_in_files
        self.allow_duplicates_in_dirs = allow_duplicates_in_dirs
        self.allow_duplicates_out_files = allow_duplicates_out_files
        self.allow_duplicates_out_dirs = allow_duplicates_out_dirs
        self.allow_duplicates_tmp_files = allow_duplicates_tmp_files
        self.print_note = print_note

        self._prepare_paths()

    # Properties

    @property
    def npaths(self):
        return sum(self.collection_sizes().values())

    @property
    def collection_sizes(self):
        return {
            coll: self.get_collection_size(coll)
            for coll in InOutPaths.COLLECTION_NAMES
        }

    def get_collection_size(self, collection):
        coll = self.get_collection(collection)
        if coll is None:
            return 0
        return len(coll)

    # Getters and setters

    def get_collection(self, collection):
        assert isinstance(collection, str)
        self._check_collection_name(collection)
        return self._collections[collection]

    def set_collection(self, name, coll):
        # NOTE: Avoid internal use
        # as it may cause an infinite loop with
        # `self._prepare_paths()`
        self._set_collection(name=name, coll=coll)
        # Ensure consistency
        self._prepare_paths()

    def _set_collection(self, name, coll):
        assert isinstance(name, str)
        assert coll is None or isinstance(coll, dict)
        if name not in InOutPaths.COLLECTION_NAMES:
            raise ValueError(
                f"`name` was not one of the allowed collection names: {InOutPaths.COLLECTION_NAMES}")
        self._collections[name] = coll

    def _update_collection(self, paths, collection):
        assert isinstance(paths, dict)
        assert isinstance(collection, str)
        self._check_collection_name(collection)
        if self._collections[collection] is None:
            self._set_collection(name=collection, coll=paths)
        self._collections[collection].update(paths)

    def __getitem__(self, name):
        """
        Get path from its key:

        e.g. d['key']
        """
        return self.get_path(name=name)

    def get_path(self, name, as_str=False, raise_on_fail=True):
        if name in self.all_paths:
            return self._format_path_out(path=self.all_paths[name], as_str=as_str)
        if raise_on_fail:
            raise ValueError(
                f"{name} was not a known key in any of the path collections.")
        return None

    def set_path(self, name, path, collection):
        # NOTE: Avoid internal use
        # as it may cause an infinite loop
        assert isinstance(name, str)
        assert isinstance(path, (str, pathlib.PurePath))
        self._update_collection(
            paths={name: path}, collection=collection)

        # Ensure consistency
        self._prepare_paths()

    def set_paths(self, paths, collection):
        # NOTE: Avoid internal use
        # as it may cause an infinite loop
        self._update_collection(paths=paths, collection=collection)

        # Ensure consistency
        self._prepare_paths()

    # Handle paths

    def check_paths(self):
        """
        Call path checks manually. These checks are automatically 
        called after each mutation with setter methods, but when
        overwriting attributes (like check settings) manually, we may need 
        to call it externally.
        """
        self._prepare_paths()

    def _prepare_paths(self):

        # Prepare paths
        in_files, in_dirs, out_files, out_dirs, tmp_files, all_paths = prepare_in_out_paths(
            in_files=self.get_collection("in_files"),
            in_dirs=self.get_collection("in_dirs"),
            out_files=self.get_collection("out_files"),
            out_dirs=self.get_collection("out_dirs"),
            tmp_files=self.get_collection("tmp_files"),
            allow_none=self.allow_none,
            allow_overwriting=self.allow_overwriting,
            allow_duplicates_in_files=self.allow_duplicates_in_files,
            allow_duplicates_in_dirs=self.allow_duplicates_in_dirs,
            allow_duplicates_out_files=self.allow_duplicates_out_files,
            allow_duplicates_out_dirs=self.allow_duplicates_out_dirs,
            allow_duplicates_tmp_files=self.allow_duplicates_tmp_files,
            pathlib_out=True)

        # Assign updated collections
        self._set_collection("in_files", in_files)
        self._set_collection("in_dirs", in_dirs)
        self._set_collection("out_files", out_files)
        self._set_collection("out_dirs", out_dirs)
        self._set_collection("tmp_files", tmp_files)
        self.all_paths = all_paths

    def mk_output_dirs(self, collection=None, verbose=True):

        # Find which collections to create output dirs for
        mkdirs_for_out_files = True
        mkdirs_for_out_dirs = True
        mkdirs_for_tmp_files = True
        if collection is not None:
            if collection not in ["out_dirs", "out_files", "tmp_files"]:
                raise ValueError(
                    f"`collection` must be one of the output path collections but was {collection}.")
            if collection != "out_files":
                mkdirs_for_out_files = False
            if collection != "out_dirs":
                mkdirs_for_out_files = False
            if collection != "tmp_files":
                mkdirs_for_tmp_files = False

        # Create output directories if they don't exist

        # For output directories
        if mkdirs_for_out_dirs:
            out_dirs = self.get_collection("out_dirs")
            if out_dirs is None:
                raise ValueError("`out_dirs` collection was `None`.")
            for k, v in out_dirs.items():
                mk_dir(path=v, arg_name=k, verbose=verbose)

        # For output files' directories
        if mkdirs_for_out_files:
            out_files = self.get_collection("out_files")
            if out_files is None:
                raise ValueError("`out_files` collection was `None`.")
            for k, v in out_files.items():
                # Get directory the file should be place in
                dir_path = pathlib.Path(v).parent
                mk_dir(path=dir_path, arg_name=k, verbose=verbose)

        # For tmp files' directories
        if mkdirs_for_tmp_files:
            tmp_files = self.get_collection("tmp_files")
            if tmp_files is None:
                raise ValueError("`tmp_files` collection was `None`.")
            for k, v in tmp_files.items():
                # Get directory the file should be place in
                dir_path = pathlib.Path(v).parent
                mk_dir(path=dir_path, arg_name=k, verbose=verbose)

    def rm_file(self, name):
        """
        Delete file from the disk.
        """
        path = self[name]
        if path is None:
            raise ValueError(f"Path object for `{name}` was `None`.")
        if not path.is_file():
            raise RuntimeError(
                f"Path for `{name}` was not an existing file: {path}")
        os.remove(str(path))

    def update(self, other):
        assert isinstance(other, InOutPaths)
        for coll_name in InOutPaths.COLLECTION_NAMES:
            self._update_collection(
                paths=other.get_collection(collection=coll_name),
                collection=coll_name
            )

        # Ensure consistency
        self._prepare_paths()

    def difference(self, other):
        """
        Find the combinations of keys and paths in the collections of this object
        that are not in the collections of the other object.
        Creates a new `InOutPaths` object with the settings from this object.
        """
        assert isinstance(other, InOutPaths)
        diff_dicts = {}
        for coll_name in InOutPaths.COLLECTION_NAMES:
            this_coll = self.get_collection(collection=coll_name)
            if this_coll is None:
                diff_dicts[coll_name] = None
                continue
            other_coll = other.get_collection(collection=coll_name)
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
            tmp_files=diff_dicts["tmp_files"]
        )

    def _new(self, in_files=None, in_dirs=None, out_files=None, out_dirs=None, tmp_files=None):
        """
        Create new `InOutPaths` object with new collections but
        keeping the rest of the settings.
        """
        return InOutPaths(
            in_files=in_files,
            in_dirs=in_dirs,
            out_files=out_files,
            out_dirs=out_dirs,
            tmp_files=tmp_files,
            allow_none=self.allow_none,
            allow_overwriting=self.allow_overwriting,
            allow_duplicates_in_files=self.allow_duplicates_in_files,
            allow_duplicates_in_dirs=self.allow_duplicates_in_dirs,
            allow_duplicates_out_files=self.allow_duplicates_out_files,
            allow_duplicates_out_dirs=self.allow_duplicates_out_dirs,
            allow_duplicates_tmp_files=self.allow_duplicates_tmp_files,
            print_note=self.print_note
        )

    def _check_collection_name(self, name):
        if name not in InOutPaths.COLLECTION_NAMES:
            raise ValueError(f"Collection name was unknown: {name}.")

    def _format_path_out(self, path, as_str):
        if as_str:
            path = str(path)
        return path

    def __str__(self) -> str:
        max_paths_per_coll = 10
        lines = []
        lines.append("Input and output paths")
        for coll_name in InOutPaths.COLLECTION_NAMES:
            collection = self.get_collection(collection=coll_name)
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
