

import time
from typing import Union
import numpy as np
import pandas as pd

from .format_time import format_time_hhmmss


class Timestamps:

    def __init__(self) -> None:
        """
        Container for storing timestamps
        and calculating the difference between two
        timestamps (e.g. the latest 2).
        """
        self.timestamps = []
        self.name_to_idx = {}
        self.idx_to_name = {}

    def __len__(self) -> int:
        """
        Number of stored timestamps.
        """
        return len(self.timestamps)

    def __eq__(self, other: object) -> bool:
        """
        Equality test.

        Checks whether the list of timestamps and the dict 
        mapping `stamp name -> index` are equal.

        Parameters
        ----------
        other : `Timestamps`
            Another `Timestamps` collection.

        Returns
        -------
        bool
            Whether the two `Timestamps` collections are equal.
        """
        return (
            self.timestamps == other.timestamps
            and self.name_to_idx == other.name_to_idx
        )

    def __getitem__(self, idx_or_name: Union[str, int]) -> int:
        """
        Get numeric timestamp (as recorded with `time.time()`)
        by indexing (via idx or name) in square brackets.

        Parameters
        ----------
        idx_or_name : int or str
            Index or name of timestamp.
        """
        assert isinstance(idx_or_name, (str, int))
        key = "idx" if isinstance(idx_or_name, int) else "name"
        return self.get_stamp(**{key: idx_or_name}, as_str=False)

    def __str__(self) -> str:
        string = "Timestamps:\n\n"
        return string + self.to_data_frame().to_string(max_rows=30) + "\n"

    def _stamp(self) -> None:
        """
        Add current time to list of timestamps.
        """
        t = time.time()
        self.timestamps.append(t)

    def stamp(self, name: str = None) -> None:
        """
        Add current time to list of timestamps.

        *Optionally* save the timestamp index with a name in the 
        `name_to_idx` dictionary to allow easy extraction later. 
        E.g. use to get the time difference between
        two larger blocks of code with in-between timestamps.

        Parameters
        ----------
        name : str
            (Optional) Unique name to store the index of the timestamp with.
        """
        self._stamp()
        if name is not None:
            if name in self.name_to_idx:
                raise ValueError("`name` was already used. Use a unique name.")
            idx = len(self) - 1
            self.name_to_idx[name] = idx
            self.idx_to_name[idx] = name

    def get_stamp(self, idx: Union[int, None] = None, name: Union[str, None] = None, as_str: bool = True) -> Union[int, str]:
        """
        Get specific timestamp from either the index or name it was recorded under.

        Note: The raw list of timestamps are also available as `.timestamps` 
        while the `name->index` dict is available as 
        `.name_to_idx`.

        Parameters
        ----------
        idx : int
            Index of the timestamp to get.
        name : str
            Name of the timestamp.
        as_str : bool
            Whether to format the difference as a string.

        Returns
        -------
        int or str
            Timestamp made with `time.time()`. 
            Optionally formatted as a string with hh:mm:ss.
        """
        if sum([idx is not None, name is not None]) != 1:
            raise ValueError(
                "Exactly one of `idx` and `name` should be specified.")
        if idx is not None:
            t = self.timestamps[idx]
        else:
            if name not in self.name_to_idx:
                raise KeyError(f"`name` '{name}' was not found.")
            t = self.timestamps[self.get_stamp_idx(name=name)]
        if as_str:
            t = format_time_hhmmss(t)
        return t

    def get_stamp_idx(self, name: str) -> int:
        """
        Get timestamp index from name of timestamp.

        Parameters
        ----------
        name : str
            Name used to store index of timestamp with.

        Returns
        -------
        int
            Index of timestamp stored with `name`.
        """
        if name not in self.name_to_idx:
            raise KeyError(f"`name` '{name}' was not found.")
        return self.name_to_idx[name]

    def get_stamp_name(self, idx: int) -> str:
        """
        Get timestamp name from index of timestamp.

        Parameters
        ----------
        idx : int
            Index of timestamp to get name for.

        Returns
        -------
        str or None
            Name of timestamp at the given index.
            When no name was recorded, `None` is returned.
        """
        if np.abs(idx) > len(self) - 1:
            raise ValueError(
                f"`idx` was out of bounds: '{idx}'. Currently stores {len(self)} timestamps.")
        return self.idx_to_name.get(idx, None)

    def to_data_frame(self):
        """
        Get times as `pandas.DataFrame` with columns [`Name`, `Time`].

        Returns
        -------
        `pandas.DataFrame`
            Data frame with names and times in the recorded order.
        """
        names = [""] * len(self)
        for idx, name in self.idx_to_name.items():
            names[idx] = name
        times = self.timestamps.copy()
        times_from_start = [t - times[0] for t in times]
        times_from_start = [format_time_hhmmss(t) for t in times_from_start]
        return pd.DataFrame({
            "Name": names,
            "Time Raw": times,
            "Time From Start": times_from_start
        })

    def took(self, start: Union[int, str] = -2, end: Union[int, str] = -1,
             as_str: bool = True, raise_negative: bool = True) -> Union[int, str]:
        """
        Get the difference between two timestamps.
        By default, the two latest timestamps are used.

        Parameters
        ----------
        start : int or str
            Either:
                1) The index of the starting timestamp.
                2) The name of the starting timestamp.
        end_idx : int or str
            Either:
                1) The index of the end timestamp.
                2) The name of the end timestamp.
        as_str : bool
            Whether to format the difference as a string.
        raise_negative : bool
            Whether to raise an error when the time difference
            between the two stamps are negative.
            In thus case, `end` came before `start`.
            When `False`, a negative number is returned.

        Returns
        -------
        int or str
            Difference in time between two given timestamps,
            either as a number or a formatted string.
        """
        start_time = self.get_stamp(
            idx=None if not isinstance(start, int) else start,
            name=None if not isinstance(start, str) else start,
            as_str=False
        )
        end_time = self.get_stamp(
            idx=None if not isinstance(end, int) else end,
            name=None if not isinstance(end, str) else end,
            as_str=False
        )
        diff = end_time - start_time
        if diff < 0 and raise_negative:
            raise ValueError((
                "Difference between timestamps was negative. "
                "`start` should correspond to an earlier timestamp than `end` "
                "(or disable `raise_negative`)."))
        if as_str:
            return format_time_hhmmss(diff)
        return diff

    def get_total_time(self, as_str: str = True) -> Union[int, str]:
        """
        Get the time difference between the first and last timestamps.

        Parameters
        ----------
        as_str : bool
            Whether to format the difference as a string.

        Returns
        -------
        int
            Difference in time between first and last timestamp,
            either as a number or a formatted string.
        """
        return self.took(
            start=0,
            end=-1,
            as_str=as_str
        )

    def update(self, other: object):
        """
        Update existing `Timestamps` collection with another `Timestamps` collection.
        Combines the list of timestamps (sorted by time) and updates the name->idx and idx->name maps,
        which is likely to change the indices.

        When both collections have the same key in the `.name_to_idx` and `.idx_to_name` dicts,
        the member from `other` is used.

        Parameters
        ----------
        other : `Timestamps` object
            Another `Timestamps` collection to combine with the current collection.
        """
        self.merge(other=other, suffix_identical_names=False)

    def merge(self, other: object, suffix_identical_names: bool = True):
        """
        Merge this `Timestamps` collection with another `Timestamps` collection.
        Combines the list of timestamps (sorted by time) and updates the name->idx and idx->name maps,
        which is likely to change the indices.

        By default, clashing names are suffixed with "_0" (this) and "_1" (other).
        If this does not lead to unique names, the suffix increases by one ("_2", "_3", "_4", ...)
        until it does.

        Parameters
        ----------
        other : `Timestamps` object
            Another `Timestamps` collection to combine with the current collection.
        suffix_identical_names : bool
            Whether to add a suffix ("_0", "_1", etc.) to clashing names
            with an increasing count until names are unique.
            When `False`, the dict members in `.name_to_idx` and `.idx_to_name` 
            from `other` is used.
        """
        # Add the two timestamps lists together
        # but as tuples with indices and an identifier
        # of which collection it came from
        combined_timestamps = \
            _list_to_enumerated_tuple(
                l=self.timestamps, identifier="this") + \
            _list_to_enumerated_tuple(
                l=other.timestamps, identifier="other")

        # Sort by ascending time
        combined_timestamps = sorted(combined_timestamps, key=lambda x: x[0])

        # Update name->index maps
        colls = {"this": self, "other": other}
        for new_idx, (_, old_idx, coll_id) in enumerate(combined_timestamps):
            coll = colls[coll_id]
            name = coll.idx_to_name.get(old_idx, None)
            if name is not None:
                coll.name_to_idx[name] = new_idx

        # Handle clashing names
        # Either by suffixing or overwriting
        if suffix_identical_names:
            # Find the clashing names
            all_names = list(self.name_to_idx.keys()) + \
                list(other.name_to_idx.keys())
            duplicate_names = set(self.name_to_idx.keys()).intersection(
                other.name_to_idx.keys())
            if duplicate_names:
                for coll in [self, other]:
                    for name in duplicate_names:
                        new_name = _create_unique_name(name, all_names)
                        all_names += [new_name]
                        coll.name_to_idx[new_name] = coll.name_to_idx.pop(name)

        # Update the dict
        self.name_to_idx.update(other.name_to_idx)

        # Create idx_to_name dict
        self.idx_to_name = {v: k for k, v in self.name_to_idx.items()}

        # Assign the combined timestamps
        self.timestamps = [x[0] for x in combined_timestamps]


def _list_to_enumerated_tuple(l, identifier):
    def make_tuple(t, i, identifier):
        if identifier is None:
            return (t, i)
        return (t, i, identifier)
    return [make_tuple(t, i, identifier) for i, t in enumerate(l)]


def _create_unique_name(name, l):
    # Add underscore
    name += "_"
    counter = 0
    while name + str(counter) in l:
        counter += 1
    return name + str(counter)
