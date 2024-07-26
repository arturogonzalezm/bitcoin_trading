"""
Unit tests for the setup_logging function in the bitcoin_trading.utils module.
"""

import logging
import pytest

from bitcoin_trading.utils import setup_logging


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Fixture to reset logging configuration after each test.
    """
    yield
    logger = logging.getLogger('bitcoin_trading.utils')
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)


def test_setup_logging_returns_logger():
    """
    Test that setup_logging returns a logger instance.
    """
    logger = setup_logging()
    assert isinstance(logger, logging.Logger)


def test_setup_logging_sets_level_to_info():
    """
    Test that setup_logging sets the logger level to INFO.
    """
    logger = setup_logging()
    assert logger.level == logging.INFO


def test_setup_logging_adds_handler():
    """
    Test that setup_logging adds a StreamHandler to the logger.
    """
    logger = setup_logging()
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_setup_logging_sets_formatter():
    """
    Test that setup_logging sets the correct formatter for the logger handler.
    """
    logger = setup_logging()
    handler = logger.handlers[0]
    assert isinstance(handler.formatter, logging.Formatter)
    # Accessing a protected member for test purposes
    assert handler.formatter._fmt == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # pylint: disable=protected-access


def test_setup_logging_does_not_add_multiple_handlers():
    """
    Test that setup_logging does not add multiple handlers if called multiple times.
    """
    logger = setup_logging()
    initial_handler_count = len(logger.handlers)
    setup_logging()  # Call the function again
    assert len(logger.handlers) == initial_handler_count


def test_setup_logging_uses_module_name():
    """
    Test that setup_logging sets the logger name to 'bitcoin_trading.utils'.
    """
    logger = setup_logging()
    assert logger.name == 'bitcoin_trading.utils'


def test_setup_logging_output(caplog):
    """
    Test that setup_logging produces the correct log output.
    """
    logger = setup_logging()
    with caplog.at_level(logging.INFO):
        logger.info("Test message")
    assert "Test message" in caplog.text
    assert "INFO" in caplog.text
    assert "bitcoin_trading.utils" in caplog.text


if __name__ == "__main__":
    pytest.main()
