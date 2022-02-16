

from utipy.time.format_time import format_time_hhmmss


def test_format_time_hhmmss():

    # t is in seconds
    format_time_hhmmss(0) == "00:00:00"
    format_time_hhmmss(10000) == "02:46:40"
