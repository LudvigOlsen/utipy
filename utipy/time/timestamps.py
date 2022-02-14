
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
        self.special_stamp_name_to_idx = {}

    def __len__(self) -> int:
        """
        Number of stored timestamps.
        """
        return len(self.timestamps)

    def stamp(self):
        """
        Add current time to list of timestamps.
        """
        t = time.time()
        self.timestamps.append(t)

    def special_stamp(self, name: str) -> None:
        """
        Add current time to list of timestamps and
        save the timestamp index with a name in the 
        `special_stamp_name_to_idx` dictionary.

        Can be used to get time difference between
        two larger blocks of code with in-between timestamps.

        Parameters
        ----------
        name : str
            Unique name to store index of timestamp with.
        """
        self.stamp()
        if name in self.special_stamp_name_to_idx:
            raise ValueError("`name` was already used. Use a unique name.")
        self.special_stamp_name_to_idx[name] = len(self) - 1

    def get_stamp(self, idx: Union[int, None] = None, name: Union[str, None] = None, as_string: bool = True) -> Union[int, str]:
        """
        Get specific timestamp from either 1) the index it was recorded under or 
        2) the special stamp name (when recorded with `.special_stamp()`).

        Note: The raw list of timestamps are also available as `.timestamps` 
        while the special time stamp name to index dict is available as 
        `.special_stamp_name_to_idx`.

        Parameters
        ----------
        idx : int
            Index of the timestamp to get.
        name : str
            Name the (special) timestamp was saved under.
            See `.special_stamp()`.
        as_string : bool
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
            t = self.get_special_stamp_idx(name=name)
        if as_string:
            t = format_time_hhmmss(t)
        return t

    def get_special_stamp_idx(self, name: str) -> int:
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
        if name not in self.special_stamp_name_to_idx:
            raise ValueError("`name` was not a known name.")
        return self.special_stamp_name_to_idx[name]

    def took(self, start_idx: int = -2, end_idx: int = -1, as_string: bool = True) -> Union[int, str]:
        """
        Get the difference between two timestamps.
        By default, the two latest timestamps are used.

        Parameters
        ----------
        start_idx : int
            The index of the starting timestamp.
        end_idx : int
            The index of the starting timestamp.
        as_string : bool
            Whether to format the difference as a string.

        Returns
        -------
        int or str
            Difference in time between two given timestamps,
            either as a number or a formatted string.
        """
        diff = self.timestamps[end_idx] - self.timestamps[start_idx]
        if diff < 0:
            raise ValueError((
                "Difference between timestamps was negative. "
                "`start_idx` should correspond to an earlier timestamp than `end_idx`."))
        if as_string:
            return format_time_hhmmss(diff)
        return diff

    def get_total_time(self, as_string: str = True) -> Union[int, str]:
        """
        Get the time difference between the first and last timestamps.

        Parameters
        ----------
        as_string : bool
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
            as_string=as_string
        )
