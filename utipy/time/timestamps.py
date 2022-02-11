
import time

from .format_time import format_time_hhmmss


class Timestamps:

    def __init__(self) -> None:
        """
        Container for storing timestamps
        and calculating the difference between two
        timestamps (e.g. the latest 2).
        """
        self.timestamps = []
        self.special_stamp_name_to_idx = {}

    def __len__(self):
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

    def special_stamp(self, name):
        """
        Add current time to list of timestamps and
        save the timestamp index with a name in the 
        `special_stamp_name_to_idx` dictionary.

        Can be used to get time difference between
        two larger blocks of code with in-between timestamps.

        :param name: Unique name to store index of timestamp with.
        """
        self.stamp()
        if name in self.special_stamp_name_to_idx:
            raise ValueError("`name` was already used. Use a unique name.")
        self.special_stamp_name_to_idx[name] = len(self) - 1

    def get_special_stamp_idx(self, name):
        """
        Get timestamp index from name of special timestamp.

        :param name: Name used to store index of timestamp with.
        :returns: Index of special timestamp stored with `name`.
        """
        if name not in self.special_stamp_name_to_idx:
            raise ValueError("`name` was not a known name.")
        return self.special_stamp_name_to_idx[name]

    def took(self, start_idx=-2, end_idx=-1, as_string=True):
        """
        Get the difference between two timestamps.
        By default, the two latest timestamps are used.

        :param start_idx: The index of the starting timestamp.
        :param end_idx: The index of the starting timestamp.
        :param as_string: Whether to format the difference as a string.
        :returns: Difference in time between two given timestamps,
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

    def get_total_time(self, as_string=True):
        """
        Get the time difference between the first and last timestamps.

        :param as_string: Whether to format the difference as a string.
        :returns: Difference in time between first and last timestamp,
            either as a number or a formatted string.
        """
        return self.took(
            start_idx=0,
            end_idx=-1,
            as_string=as_string
        )
