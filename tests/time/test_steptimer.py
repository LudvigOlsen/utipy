

from time import sleep

import pytest
from utipy.time.timer import StepTimer


def test_steptimer(capfd):

    step_timer = StepTimer(message="testing took:", msg_fn=print, verbose=True)

    with step_timer.time_step(indent=8, name_prefix="first"):
        sleep(0.1)
    out, err = capfd.readouterr()
    assert out == "        testing took: 00:00:00\n"

    with pytest.raises(AssertionError):
        # Should not record anything
        with step_timer.time_step(indent=-1, name_prefix="second"):
            sleep(0.1)

    with step_timer.time_step(indent=0, name_prefix="third"):
        sleep(0.1)
    out, err = capfd.readouterr()
    assert out == "testing took: 00:00:00\n"

    # 2x start + end timestamps
    assert len(step_timer) == 4

    # Check keys are as expected
    assert set(step_timer.name_to_idx.keys()) == set([
        "first_start", "first_end",
        "third_start", "third_end"
    ])


def test_steptimer_nested(capfd):
    step_timer = StepTimer(message="testing took:", msg_fn=print, verbose=True)
    with step_timer.time_step(indent=2):
        sleep(0.1)
        with step_timer.time_step(indent=4):
            sleep(0.1)
    out, err = capfd.readouterr()
    assert out == "  testing took: 00:00:00\n    testing took: 00:00:00\n"
