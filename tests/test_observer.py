"""
This module contains tests for the Observer and BinanceSubject classes.
"""
import pytest
from unittest.mock import MagicMock
from bitcoin_trading.observer import BinanceSubject, Observer


@pytest.fixture
def caplog_fixture(caplog):
    """
    Fixture that wraps the caplog to avoid redefinition warnings.
    :param caplog: The caplog fixture provided by pytest.
    :return: The wrapped caplog fixture.
    """
    return caplog


@pytest.fixture
def binance_subject_fixture():
    """
    Fixture that provides an instance of BinanceSubject.
    :return: A new instance of BinanceSubject.
    """
    return BinanceSubject()


@pytest.fixture
def mock_observer_fixture():
    """
    Fixture that provides a mock observer.
    :return: A MagicMock instance spec'd to Observer.
    """
    observer = MagicMock(spec=Observer)
    return observer


def test_attach_new_observer(binance_subject_fixture, mock_observer_fixture, caplog_fixture):
    """
    Test attaching a new observer to the BinanceSubject.
    :param binance_subject_fixture: The BinanceSubject instance.
    :param mock_observer_fixture: The mock observer.
    :param caplog_fixture: The caplog fixture for capturing log messages.
    """
    binance_subject_fixture.attach(mock_observer_fixture)
    assert mock_observer_fixture in binance_subject_fixture._observers  # pylint: disable=protected-access
    assert "Observer" in caplog_fixture.text
    assert "attached" in caplog_fixture.text


def test_attach_existing_observer(binance_subject_fixture, mock_observer_fixture, caplog_fixture):
    """
    Test attaching an already attached observer to the BinanceSubject.
    :param binance_subject_fixture: The BinanceSubject instance.
    :param mock_observer_fixture: The mock observer.
    :param caplog_fixture: The caplog fixture for capturing log messages.
    """
    binance_subject_fixture.attach(mock_observer_fixture)
    binance_subject_fixture.attach(mock_observer_fixture)
    assert binance_subject_fixture._observers.count(mock_observer_fixture) == 1  # pylint: disable=protected-access
    assert "already attached" in caplog_fixture.text


def test_detach_existing_observer(binance_subject_fixture, mock_observer_fixture, caplog_fixture):
    """
    Test detaching an attached observer from the BinanceSubject.
    :param binance_subject_fixture: The BinanceSubject instance.
    :param mock_observer_fixture: The mock observer.
    :param caplog_fixture: The caplog fixture for capturing log messages.
    """
    binance_subject_fixture.attach(mock_observer_fixture)
    binance_subject_fixture.detach(mock_observer_fixture)
    assert mock_observer_fixture not in binance_subject_fixture._observers  # pylint: disable=protected-access
    assert "detached" in caplog_fixture.text


def test_detach_nonexistent_observer(binance_subject_fixture, mock_observer_fixture, caplog_fixture):
    """
    Test detaching a non-existent observer from the BinanceSubject.
    :param binance_subject_fixture: The BinanceSubject instance.
    :param mock_observer_fixture: The mock observer.
    :param caplog_fixture: The caplog fixture for capturing log messages.
    """
    binance_subject_fixture.detach(mock_observer_fixture)
    assert "could not detach" in caplog_fixture.text


def test_notify_observers(binance_subject_fixture, mock_observer_fixture):
    """
    Test notifying all attached observers with a message.
    :param binance_subject_fixture: The BinanceSubject instance.
    :param mock_observer_fixture: The mock observer.
    """
    message = "Test Message"
    binance_subject_fixture.attach(mock_observer_fixture)
    binance_subject_fixture.notify(message)
    mock_observer_fixture.update.assert_called_once_with(message)


if __name__ == "__main__":
    pytest.main()
