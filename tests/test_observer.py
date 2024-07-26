"""
This module contains tests for the Observer and BinanceSubject classes.
"""
import logging
import pytest

from bitcoin_trading.observer import Observer, BinanceSubject


@pytest.fixture
def caplog(caplog):
    """
    Fixture to capture log messages.
    :param caplog:
    :return:
    """
    return caplog


# Mock Observer class for testing
class MockObserver(Observer):
    """
    Mock Observer class for testing.
    """
    def __init__(self):
        """
        Constructor for the MockObserver class.
        """
        self.messages = []

    def update(self, message):
        """
        Update method for the MockObserver class.
        :param message:
        :return:
        """
        self.messages.append(message)


@pytest.fixture
def binance_subject():
    """
    Fixture to create a BinanceSubject instance.
    :return:
    """
    return BinanceSubject()


@pytest.fixture
def mock_observer():
    """
    Fixture to create a MockObserver instance.
    :return:
    """
    return MockObserver()


def test_binance_subject_initialization(binance_subject):
    """
    Test the initialization of the BinanceSubject class.
    :param binance_subject:
    :return:
    """
    assert binance_subject._observers == []


def test_attach_observer(binance_subject, mock_observer):
    """
    Test the attach method of the BinanceSubject class.
    :param binance_subject:
    :param mock_observer:
    :return:
    """
    binance_subject.attach(mock_observer)
    assert mock_observer in binance_subject._observers


def test_detach_observer(binance_subject, mock_observer):
    """
    Test the detach method of the BinanceSubject class.
    :param binance_subject:
    :param mock_observer:
    :return:
    """
    binance_subject.attach(mock_observer)
    binance_subject.detach(mock_observer)
    assert mock_observer not in binance_subject._observers


def test_notify_observers(binance_subject, mock_observer):
    """
    Test the notify method of the BinanceSubject class.
    :param binance_subject:
    :param mock_observer:
    :return:
    """
    binance_subject.attach(mock_observer)
    test_message = "Test notification"
    binance_subject.notify(test_message)
    assert mock_observer.messages == [test_message]


def test_notify_multiple_observers(binance_subject):
    """
    Test the notify method of the BinanceSubject class with multiple observers.
    :param binance_subject:
    :return:
    """
    observers = [MockObserver() for _ in range(3)]
    for observer in observers:
        binance_subject.attach(observer)

    test_message = "Test notification for multiple observers"
    binance_subject.notify(test_message)

    for observer in observers:
        assert observer.messages == [test_message]


def test_attach_logs_info(binance_subject, mock_observer, caplog):
    """
    Test that the attach method logs an info message.
    :param binance_subject:
    :param mock_observer:
    :param caplog:
    :return:
    """
    with caplog.at_level(logging.INFO):
        binance_subject.attach(mock_observer)
    assert f"Observer {mock_observer} attached" in caplog.text


def test_detach_logs_info(binance_subject, mock_observer, caplog):
    """
    Test that the detach method logs an info message.
    :param binance_subject:
    :param mock_observer:
    :param caplog:
    :return:
    """
    binance_subject.attach(mock_observer)
    with caplog.at_level(logging.INFO):
        binance_subject.detach(mock_observer)
    assert f"Observer {mock_observer} detached" in caplog.text


def test_attach_duplicate_observer(binance_subject, mock_observer):
    """
    Test that the attach method does not attach duplicate observers.
    :param binance_subject:
    :param mock_observer:
    :return:
    """
    binance_subject.attach(mock_observer)
    binance_subject.attach(mock_observer)
    assert binance_subject._observers.count(mock_observer) == 1


def test_detach_nonexistent_observer(binance_subject, mock_observer, caplog):
    """
    Test that the detach method logs a warning message when the observer is not found.
    :param binance_subject:
    :param mock_observer:
    :param caplog:
    :return:
    """
    with caplog.at_level(logging.WARNING):
        binance_subject.detach(mock_observer)
    assert f"Observer {mock_observer} not found, could not detach" in caplog.text


if __name__ == "__main__":
    pytest.main()
