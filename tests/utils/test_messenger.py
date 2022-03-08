

from utipy.utils.messenger import Messenger, check_messenger

import logging


def test_messenger_print(capfd):

    printer = Messenger(verbose=True, indent=2, msg_fn=print)

    # Default indentation
    printer("Ma name is not John",
            "Ma name is James",
            "I shall not repeat this")

    out, err = capfd.readouterr()
    assert out == "  Ma name is not John Ma name is James I shall not repeat this\n"

    # Override indentation
    printer("Ma name is not John",
            "Ma name is James",
            "I shall not repeat this", indent=4)

    out, err = capfd.readouterr()
    assert out == "    Ma name is not John Ma name is James I shall not repeat this\n"

    # Disable verbosity
    printer("Ma name is not John",
            "Ma name is James",
            "I shall not repeat this", verbose=False)

    out, err = capfd.readouterr()
    assert out == ""


def test_messenger_logger(capfd, caplog):

    logging.basicConfig()
    _logger = logging.getLogger("Mr.Logger")
    _logger.setLevel(logging.INFO)
    logger = Messenger(verbose=True, indent=2, msg_fn=_logger.info)

    # Default indentation
    logger("Ma name is not John")

    def get_last_log_message():
        for rec in caplog.records:
            pass
        return rec.getMessage()
    assert get_last_log_message() == "  Ma name is not John"

    # Override indentation
    logger("Ma name is not John", indent=4)

    assert get_last_log_message() == "    Ma name is not John"

    # Multiple args
    logger("Ma name is not John", "Ma name is James", indent=4)

    assert get_last_log_message() == "    Ma name is not John Ma name is James"

    # Disable verbosity
    logger("Ma name is not John", verbose=False)

    out, err = capfd.readouterr()
    assert out == ""


def test_check_messenger():

    messenger = Messenger(verbose=True, indent=2, msg_fn=print)
    assert check_messenger(messenger) is messenger

    class SubMessenger(Messenger):

        def __init__(self) -> None:
            super().__init__(verbose=True, msg_fn=print, indent=0)

    # Works with subclasses of Messenger
    submessenger = SubMessenger()
    assert check_messenger(submessenger) is submessenger

    # None should return Messenger with `verbose=False`
    assert isinstance(check_messenger(None), Messenger)
    assert not check_messenger(None).verbose
