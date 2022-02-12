
import os
import pathlib
from itertools import combinations


# TODO Test (e.g. with "-" path included)
# TODO Add checks of path validity (bad symbols etc.) - Perhaps pathlib.Path does that?
# TODO allow checking if output is nested in input dir
# TODO Perhaps check compatibility on windows and other platforms

def prepare_in_out_paths(
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
    allow_duplicates_tmp_files=False,
    pathlib_out=True
):
    """
    Checks paths and converts them to `pathlib.Path` objects.
    Creates missing output directories.

    Note: Even when `allow_overwriting` is enabled, 
    `in_files` and `out_files` cannot contain the same paths.

    Keys must be unique across the dictionaries.

    :param in_files: Dict mapping argument name -> input filepath.
        A path can also be "-" when streaming input. 
        This value will remain a string and will not be checked
        for duplication, existence, etc.
    :param in_dirs: Dict mapping argument name -> input directory path.
    :param out_files: Dict mapping argument name -> output filepath.
    :param out_dirs: Dict mapping argument name -> output directory path.
    :param allow_none: Whether to allow paths (i.e. dict values) to be `None`,
        in which case they will be ignored.
    :param allow_overwriting: Whether to allow `out_files` paths 
        to already exist.
    :param allow_duplicates_in_files: Whether to allow duplicate
        values (i.e. paths) in `in_files`.
    :param allow_duplicates_in_dirs: Whether to allow duplicate
        values (i.e. paths) in `in_dirs`.
    :param allow_duplicates_out_files: Whether to allow duplicate
        values (i.e. paths) in `out_files`.
    :param allow_duplicates_out_dirs: Whether to allow duplicate
        values (i.e. paths) in `out_dirs`.
    :param pathlib_out: Whether to convert the paths to 
        `pathlib.Path` objects on return.
    :returns: Updated dicts (or `None`) for `in_files`, `in_dirs`, `out_files` and `out_dirs`.
        Paths are `pathlib.Path` objects that have been "resolved".
    """

    # Check keys are unique

    # Add collections to a named dict
    named_collections = {
        "in_files": in_files,
        "out_files": out_files,
        "in_dirs": in_dirs,
        "out_dirs": out_dirs,
        "tmp_files": tmp_files
    }

    # Assert non-overlapping keys in all combinations of collections
    for k1, k2 in set(combinations(named_collections.keys(), 2)):
        _check_different_keys(
            named_collections[k1],
            named_collections[k2],
            names=[k1, k2]
        )

    # Check paths in dicts

    # Check input filepaths
    in_files = _check_paths_dict(
        d=in_files,
        d_name="in_files",
        allow_none=allow_none,
        check_duplicates=not allow_duplicates_in_files,
        assert_exists=True,
        path_type="file"
    )

    # Check output filepaths
    out_files = _check_paths_dict(
        d=out_files,
        d_name="out_files",
        allow_none=allow_none,
        check_duplicates=not allow_duplicates_out_files,
        assert_exists=False,
        assert_missing=not allow_overwriting,
        path_type="file"
    )

    # Check tmp filepaths
    tmp_files = _check_paths_dict(
        d=tmp_files,
        d_name="tmp_files",
        allow_none=allow_none,
        check_duplicates=not allow_duplicates_tmp_files,
        assert_exists=False,
        assert_missing=not allow_overwriting,
        path_type="file"
    )

    # Check input directory paths
    in_dirs = _check_paths_dict(
        d=in_dirs,
        d_name="in_dirs",
        allow_none=allow_none,
        check_duplicates=not allow_duplicates_in_dirs,
        assert_exists=True,
        path_type="directory"
    )

    # Check output directory paths
    out_dirs = _check_paths_dict(
        d=out_dirs,
        d_name="out_dirs",
        allow_none=allow_none,
        check_duplicates=not allow_duplicates_out_dirs,
        path_type="directory"
    )

    # Check for path duplicates across file collections
    _check_duplicates_across_dicts(d1=in_files, d2=out_files)
    _check_duplicates_across_dicts(d1=in_files, d2=tmp_files)
    _check_duplicates_across_dicts(d1=out_files, d2=tmp_files)

    # Convert all paths to pathlib.Path objects
    if pathlib_out:
        in_files = _normalize_paths(in_files, type_fn=pathlib.Path)
        in_dirs = _normalize_paths(in_dirs, type_fn=pathlib.Path)
        out_files = _normalize_paths(out_files, type_fn=pathlib.Path)
        out_dirs = _normalize_paths(out_dirs, type_fn=pathlib.Path)
        tmp_files = _normalize_paths(tmp_files, type_fn=pathlib.Path)

    # Combine collections to single dict
    # for faster and simpler look-up
    # Hence the need for unique keys
    # across the dicts
    specified_collections = [
        coll for coll in [in_files, in_dirs, out_files, out_dirs, tmp_files]
        if coll is not None
    ]
    for i, coll in enumerate(specified_collections):
        if i == 0:
            all_paths = coll.copy()
        else:
            all_paths.update(coll)

    return in_files, in_dirs, out_files, out_dirs, tmp_files, all_paths


# Utilities

def _check_paths_dict(d, d_name, allow_none=False, check_duplicates=True,
                      assert_exists=False, assert_missing=False, path_type="file"):
    if assert_exists and assert_missing:
        raise ValueError(
            "Both `assert_exists` and `assert_missing` were enabled.")

    if d is not None:
        if not (d is None or isinstance(d, dict)):
            raise ValueError(
                f"{d_name} must be either a `dict` of paths or `None`.")
        if allow_none:
            d = _rm_none_elements(d)
        _check_elements(d)
        # Convert to string
        d = _normalize_paths(d, type_fn=str)
        if check_duplicates:
            _check_duplicates(d)
        if assert_exists or assert_missing:
            _check_paths_exist(
                d,
                check_type=path_type,
                raise_when="unknown" if assert_exists else "known"
            )
    return d


def _rm_none_elements(d):
    if d is not None:
        return {k: v for k, v in d.items() if v is not None}
    else:
        return None


def _normalize_paths(d, type_fn=str):
    def path_formatter(v):
        if isinstance(v, str) and v == "-":
            return str(v)
        else:
            return type_fn(pathlib.Path(v).resolve())

    if d is not None:
        # Convert to full paths as strings
        return {k: path_formatter(v) for k, v in d.items()}
    return None


def _check_elements(d):
    if d is not None:

        # Check values
        invalid_keys = [
            k for k, v in d.items()
            if not isinstance(v, (str, pathlib.PurePath))
        ]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"The following paths were of an invalid type: {invalid_keys}.")

        # Check keys are strings
        invalid_keys = [
            k for k in d.keys()
            if not isinstance(k, str)
        ]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"The following keys were of an invalid type: {invalid_keys}. Keys must be strings.")


def _find_duplicate_value_to_keys(d):
    unique_values = set([str(v) for v in d.values()])
    if "-" in unique_values:
        unique_values = unique_values.difference(set("-"))
    # This might be slow with large dictionaries
    value_to_keys = {uv: [k for k, v in d.items() if str(v) == uv]
                     for uv in unique_values}
    duplicates = {v: ks for v, ks in value_to_keys.items() if len(ks) > 1}
    if len(duplicates) > 0:
        return duplicates
    return {}


def _check_duplicates(d):
    if d is not None:
        if len(set(d.values())) != len(d.values()):
            duplicate_keys = _find_duplicate_value_to_keys(d).keys()
            if len(duplicate_keys) > 0:
                # Reason for extra check:
                #   Could have been multiple "-" paths
                #   which would have been okay
                raise ValueError(
                    f"Found duplicate paths for the following arguments: {duplicate_keys}")


def _check_paths_exist(d, check_type="file", raise_when="unkown"):
    assert raise_when in ["unknown", "known"]
    assert check_type in ["file", "directory"]
    check_fn = os.path.isfile if check_type == "file" else os.path.isdir
    for k, v in d.items():
        if str(v) == "-":
            continue
        if raise_when == "unknown":
            assert check_fn(str(v)), \
                f"`{k}` was not a {check_type}."
        else:
            assert not check_fn(str(v)), \
                f"`{k}` is an existing {check_type}."


def _check_duplicates_across_dicts(d1, d2):

    if d1 is None or d2 is None:
        return None

    # Copy to ensure we don't alter
    # original dicts in parent scope
    d1 = d1.copy()
    d2 = d2.copy()

    # Deduplicate each dict internally

    # Find keys to remove
    d1_duplicates_keys_to_remove = [
        k for _, keys in _find_duplicate_value_to_keys(d1)
        for k in keys[1:]]
    d2_duplicates_keys_to_remove = [
        k for _, keys in _find_duplicate_value_to_keys(d2)
        for k in keys[1:]]

    # Remove the keys
    for k in d1_duplicates_keys_to_remove:
        del d1[k]
    for k in d2_duplicates_keys_to_remove:
        del d2[k]

    # Combine the two dictionaries
    combined = d1
    combined.update(d2)

    # Check for duplicate values across the two dictionaries
    _check_duplicates(combined)


def _check_different_keys(d1, d2, names):
    if d1 is not None and d2 is not None:
        key_intersection = list(
            set(d1.keys()).intersection(
                set(d2.keys())
            )
        )
        # Raise error if any intersection
        if len(key_intersection):
            raise ValueError(
                f"The same keys were found in `{names[0]}` and `{names[1]}`: {key_intersection}.")
