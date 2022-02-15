
import time
from typing import Union

from .format_time import format_time_hhmmss

# TODO Add tests


class Timestamps:

    def __init__(self) -> None:
        """
        Container for storing timestamps
        and calculating the difference between two
        timestamps (e.g. the latest 2).
        """
        self.timestamps = []
        self.name_to_idx = {}

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
        if name in self.name_to_idx:
            raise ValueError("`name` was already used. Use a unique name.")
        self.name_to_idx[name] = len(self) - 1

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
            t = self.timestamps[self.get_stamp_idx(name=name)]
        if as_str:
            t = format_time_hhmmss(t)
        return t

    def get_stamp_idx(self, name: str) -> int:
        """
        Get timestamp index from name of special timestamp.

        Parameters
        ----------
        name : str
            Name used to store index of special timestamp with.

        Returns
        -------
        int
            Index of special timestamp stored with `name`.
        """
        if name not in self.name_to_idx:
            raise ValueError(f"`name` was not a known name: '{name}'.")
        return self.name_to_idx[name]

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
            start_idx=0,
            end_idx=-1,
            as_str=as_str
        )
