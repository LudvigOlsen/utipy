
from numbers import Number
import numpy as np


def format_time_hhmmss(t: int) -> str:
    """
    Format a count of seconds into hh:mm:ss where hh is allowed to be >24.

    NOTE: As `time.strftime(fmt, time.gmtime(t))` is not perfect when dealing with multiday running times
    we just wrote our own formatting that allows >24 hours. We don't need to split into days.
    Only 2x in speed, so does not affect running time in practice. (5000 runs < 0.1s)

    Parameters
    ----------
    t : int
        Timepoint as found with `time.time()`.

    Returns
    -------
    str
        The timepoint formatted as a hh:mm:ss string.
    """
    # Hours
    hours = np.floor(t / 60 / 60)
    hours_seconds = hours * 60 * 60

    # Minutes
    mins = np.floor((t - hours_seconds) / 60)
    mins_seconds = mins * 60

    # Seconds
    secs = (t - hours_seconds - mins_seconds)

    return f"{_format_part(hours)}:{_format_part(mins)}:{_format_part(secs)}"


def _format_part(t: Number) -> str:
    """
    Format integer-like number as 2-digit string (either hh, mm, or ss).

    Parameters
    ----------
    t : Number
        A 1- or 2-digit number (after conversion to integer).

    Returns
    -------
    str
        A two-character string. From "00" -> "99".
    """
    t = int(t)
    if t == 0:
        return "00"
    if t < 10:
        return "0" + str(t)
    return str(t)
