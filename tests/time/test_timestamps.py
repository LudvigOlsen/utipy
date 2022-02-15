

from time import sleep

from utipy.time.timestamps import Timestamps


def test_timestamps_number_of_stamps():
    stamper = Timestamps()
    stamper.stamp()
    sleep(0.001)
    stamper.stamp(name="second")
    sleep(0.001)
    stamper.stamp()
    sleep(0.001)
    stamper.stamp(name="fourth")
    total_time = stamper.get_total_time(as_str=True)
    assert len(stamper) == 4
    assert "second" in stamper.name_to_idx
    assert stamper.name_to_idx["second"] == 1
    assert stamper.idx_to_name[1] == "second"
    assert "fourth" in stamper.name_to_idx
    assert stamper.name_to_idx["fourth"] == 3
    assert stamper.idx_to_name[3] == "fourth"
    assert total_time == "00:00:00"  # NOTE: Could technically fail on rare occasions


def test_timestamps_merge():
    stamper_1 = Timestamps()
    stamper_2 = Timestamps()

    # Intertwined stamping

    stamper_1.stamp()
    sleep(0.001)
    stamper_1.stamp(name="second")
    sleep(0.001)

    stamper_2.stamp()
    sleep(0.001)
    stamper_2.stamp(name="second")  # Clashes
    sleep(0.001)

    stamper_1.stamp()
    sleep(0.001)
    stamper_1.stamp(name="fourth")
    sleep(0.001)

    stamper_2.stamp(name="third")
    sleep(0.001)
    stamper_2.stamp()

    stamper_1.merge(stamper_2, suffix_identical_names=True)

    assert len(stamper_1) == 8
    assert len(stamper_2) == 4
    assert stamper_1.name_to_idx == {
        "second_0": 1,
        "second_1": 3,
        "fourth": 5,
        "third": 6
    }

    df = stamper_1.to_data_frame()
    print(df)
    assert all(df["Name"] == [
        "", "second_0", "",
        "second_1", "", "fourth",
        "third", ""
    ])
    assert df["Time From Start"][0] == "00:00:00"  # Difference to first stamp

    assert stamper_1.get_stamp_idx("second_0") == 1
    assert stamper_1.get_stamp_idx("third") == 6
    assert stamper_1.get_stamp_name(1) == "second_0"
    assert stamper_1.get_stamp_name(6) == "third"