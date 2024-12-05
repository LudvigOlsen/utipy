import os
from copy import deepcopy
import pathlib
from itertools import combinations
from typing import Dict, List, Optional


# TODO Test (e.g., with "-" path included)
# TODO Add checks of path validity (bad symbols etc.) - Perhaps pathlib.Path does that?
# TODO allow checking if output is nested in input dir
# TODO Perhaps check compatibility on windows and other platforms
# TODO Convert docs to other format


def prepare_in_out_paths(
    named_collections: Dict[str, dict] = None,
    allow_none: bool = False,
    allow_overwriting: bool = True,
    allow_duplicates_in: List[str] = ["in_dirs", "out_dirs", "tmp_dirs"],
    disallowed_nestings: List[tuple] = [
        ("in_files", "tmp_dirs"),
        ("out_files", "tmp_dirs"),
        ("in_dirs", "tmp_dirs"),
        ("out_dirs", "tmp_dirs"),
    ],
    pathlib_out: bool = True,
    copy: bool = True,
):
    """
    Checks paths and converts them to `pathlib.Path` objects.
    Creates missing output directories.

    Note: Even when `allow_overwriting` is enabled,
    `in_files` and `out_files` cannot contain the same paths.

    Keys must be unique across the dictionaries.

    named_collections : dict of dicts
        A dict mapping collection name -> collection where a collection
        is a dict mapping (argument) name -> path.
        For the `in_files` collection, a path can also be "-" when streaming input.
            This value will remain a string and will not be checked
            for duplication, existence, etc.
    :param allow_none: Whether to allow paths (i.e. dict values) to be `None`,
        in which case they will be ignored.
    :param allow_overwriting: Whether to allow `out_files` paths
        to already exist.
    allow_duplicates_in : list
        List of collections to allow duplicate paths in. One of:
            {'in_files', 'in_dirs', 'out_files', 'out_dirs', 'tmp_files', 'tmp_dirs'}.
    disallowed_nestings : list of tuples
        Pairs of collections where the paths of the first cannot
        be nested inside the paths of the second.
        By default, the in and out paths cannot be located within
        the temporary directories, as these might be deleted.
    :param pathlib_out: Whether to convert the paths to
        `pathlib.Path` objects on return.
    :returns: Updated dicts (or `None`) for `in_files`, `in_dirs`, `out_files` and `out_dirs`.
        Paths are `pathlib.Path` objects that have been "resolved".
    """

    if copy:
        # Nested dictionaries -> deep copy
        named_collections = deepcopy(named_collections)

    # Check keys are unique

    # Assert non-overlapping keys in all combinations of collections
    for k1, k2 in set(combinations(named_collections.keys(), 2)):
        _check_different_keys(
            named_collections[k1], named_collections[k2], names=[k1, k2]
        )

    # Check paths in dicts

    # Check input filepaths
    named_collections["in_files"] = _check_paths_dict(
        d=named_collections["in_files"],
        d_name="in_files",
        allow_none=allow_none,
        check_duplicates="in_files" not in allow_duplicates_in,
        assert_exists=True,
        path_type="file",
    )

    # Check output filepaths
    named_collections["out_files"] = _check_paths_dict(
        d=named_collections["out_files"],
        d_name="out_files",
        allow_none=allow_none,
        check_duplicates="out_files" not in allow_duplicates_in,
        assert_exists=False,
        assert_missing=not allow_overwriting,
        path_type="file",
    )

    # Check tmp filepaths
    named_collections["tmp_files"] = _check_paths_dict(
        d=named_collections["tmp_files"],
        d_name="tmp_files",
        allow_none=allow_none,
        check_duplicates="tmp_files" not in allow_duplicates_in,
        assert_exists=False,
        assert_missing=not allow_overwriting,
        path_type="file",
    )

    # Check input directory paths
    named_collections["in_dirs"] = _check_paths_dict(
        d=named_collections["in_dirs"],
        d_name="in_dirs",
        allow_none=allow_none,
        check_duplicates="in_dirs" not in allow_duplicates_in,
        assert_exists=True,
        path_type="directory",
    )

    # Check output directory paths
    named_collections["out_dirs"] = _check_paths_dict(
        d=named_collections["out_dirs"],
        d_name="out_dirs",
        allow_none=allow_none,
        check_duplicates="out_dirs" not in allow_duplicates_in,
        path_type="directory",
    )

    # Check temporary directory paths
    named_collections["tmp_dirs"] = _check_paths_dict(
        d=named_collections["tmp_dirs"],
        d_name="tmp_dirs",
        allow_none=allow_none,
        check_duplicates="tmp_dirs" not in allow_duplicates_in,
        assert_missing=True,
        path_type="directory",
    )

    # Check for path duplicates across file collections
    # and make sure `tmp_dirs` are unique as they might be deleted after use
    to_check_for_dups = [
        ("in_files", "out_files"),
        ("in_files", "tmp_files"),
        ("out_files", "tmp_files"),
        ("tmp_dirs", "in_dirs"),
        ("tmp_dirs", "out_dirs"),
    ]
    for coll_1, coll_2 in to_check_for_dups:
        _check_duplicates_across_dicts(
            d1=named_collections[coll_1], d2=named_collections[coll_2]
        )

    # Check nestings
    # Paths in coll_1 cannot be nested within coll_2
    for coll_1, coll_2 in disallowed_nestings:
        _check_nestings(d1=named_collections[coll_1], d2=named_collections[coll_2])

    # Convert all paths to pathlib.Path objects
    if pathlib_out:
        for key, coll in named_collections.items():
            named_collections[key] = _normalize_paths(coll, type_fn=pathlib.Path)

    # Combine collections to single dict
    # for faster and simpler look-up
    # Hence the need for unique keys
    # across the dicts
    specified_collections = [
        coll for coll in named_collections.values() if coll is not None
    ]
    if not len(specified_collections):
        all_paths = {}
    for i, coll in enumerate(specified_collections):
        if i == 0:
            all_paths = coll.copy()
        else:
            all_paths.update(coll)

    return named_collections, all_paths


# Utilities


def _check_paths_dict(
    d: Optional[dict],
    d_name: str,
    allow_none: bool = False,
    check_duplicates: bool = True,
    assert_exists: bool = False,
    assert_missing: bool = False,
    path_type: str = "file",
):
    if assert_exists and assert_missing:
        raise ValueError("Both `assert_exists` and `assert_missing` were enabled.")

    if d is not None:
        if not (d is None or isinstance(d, dict)):
            raise ValueError(f"{d_name} must be either a `dict` of paths or `None`.")
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
                raise_when="unknown" if assert_exists else "known",
            )
    return d


def _rm_none_elements(d: dict):
    if d is not None:
        return {k: v for k, v in d.items() if v is not None}
    else:
        return None


def _normalize_paths(d: dict, type_fn=str):
    def path_formatter(v):
        if isinstance(v, str) and v == "-":
            return str(v)
        else:
            return type_fn(pathlib.Path(v).resolve())

    if d is not None:
        # Convert to full paths as strings
        return {k: path_formatter(v) for k, v in d.items()}
    return None


def _check_elements(d: dict):
    if d is not None:
        # Check values
        invalid_keys = [
            k for k, v in d.items() if not isinstance(v, (str, pathlib.PurePath))
        ]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"The following paths were of an invalid type: {', '.join(invalid_keys)}."
            )

        # Check keys are strings
        invalid_keys = [k for k in d.keys() if not isinstance(k, str)]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"The following keys were of an invalid type: {', '.join(invalid_keys)}. Keys must be strings."
            )


def _find_duplicate_value_to_keys(d: dict):
    unique_values = set([str(v) for v in d.values()])
    if "-" in unique_values:
        unique_values = unique_values.difference(set("-"))
    # This might be slow with large dictionaries
    value_to_keys = {
        uv: [k for k, v in d.items() if str(v) == uv] for uv in unique_values
    }
    duplicates = {v: ks for v, ks in value_to_keys.items() if len(ks) > 1}
    if len(duplicates) > 0:
        return duplicates
    return {}


def _check_duplicates(d: dict):
    if d is not None:
        if len(set(d.values())) != len(d.values()):
            # Note: `_find_duplicate_value_to_keys` returns path->keys mappings
            duplicates = _find_duplicate_value_to_keys(d).values()
            if len(duplicates) > 0:
                # Reason for extra check:
                #   Could have been multiple "-" paths
                #   which would have been okay
                raise ValueError(
                    "Found duplicate paths for some paths. "
                    "Duplicate paths had the following names: "
                    f"\n{duplicates}"
                )


def _check_paths_exist(d: dict, check_type: str = "file", raise_when: str = "unkown"):
    assert raise_when in ["unknown", "known"]
    assert check_type in ["file", "directory"]
    check_fn = os.path.isfile if check_type == "file" else os.path.isdir
    for k, v in d.items():
        if str(v) == "-":
            continue
        if raise_when == "unknown":
            assert check_fn(str(v)), f"`{k}` was not a {check_type}: {v}"
        else:
            assert not check_fn(str(v)), f"`{k}` is an existing {check_type}: {v}"


def _check_duplicates_across_dicts(d1: Optional[dict], d2: Optional[dict]):
    # TODO This requires documentation!

    if d1 is None or d2 is None:
        return None

    # Copy to ensure we don't alter
    # original dicts in parent scope
    d1 = d1.copy()
    d2 = d2.copy()

    # Deduplicate each dict internally

    # Find keys to remove
    d1_duplicates_keys_to_remove = [
        k for _, keys in _find_duplicate_value_to_keys(d1) for k in keys[1:]
    ]
    d2_duplicates_keys_to_remove = [
        k for _, keys in _find_duplicate_value_to_keys(d2) for k in keys[1:]
    ]

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


def _check_different_keys(d1: Optional[dict], d2: Optional[dict], names: list):
    if d1 is not None and d2 is not None:
        key_intersection = list(set(d1.keys()).intersection(set(d2.keys())))
        # Raise error if any intersection
        if len(key_intersection):
            raise ValueError(
                f"The same keys were found in `{names[0]}` and `{names[1]}`: {key_intersection}."
            )


def _check_nestings(d1: Optional[dict], d2: Optional[dict]):
    if d1 is not None and d2 is not None:
        nestings = _find_nested(d1, d2)
        if nestings:
            nestings_string = [f"({x} in {y})" for x, y in nestings]
            raise ValueError(
                f"Found {len(nestings)} disallowed nested paths: "
                f"{', '.join(nestings_string)}."
            )


def _find_nested(d1, d2):
    """
    Find paths in d1 that are nested inside paths in d2.

    Returns tuples with keys `(d1_key, d2_key)` where `d1_path` was a subdirectory of `d2_path`.
    """
    # Copy to ensure we don't alter
    # original dicts in parent scope
    d1 = d1.copy()
    d2 = d2.copy()

    # Make paths `pathlib.Path` objects
    d1 = _normalize_paths(d1, type_fn=pathlib.Path)
    d2 = _normalize_paths(d2, type_fn=pathlib.Path)

    return [
        (d1_key, d2_key)
        for d1_key, d1_path in d1.items()
        for d2_key, d2_path in d2.items()
        if d2_path in d1_path.parents
    ]
