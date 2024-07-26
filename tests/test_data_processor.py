"""
This module contains the tests for the DataProcessor class.
"""
import json
import time
import pytest
from bitcoin_trading.data_processor import DataProcessor


@pytest.fixture
def sample_message():
    """
    Fixture to return a sample message.
    :return: str: A sample message.
    """
    return json.dumps({
        "E": int(time.time() * 1000),
        "s": "BTCUSDT",
        "p": "0.001",
        "P": "0.1",
        "w": "45000.0",
        "x": "44999.0",
        "c": "45001.0",
        "Q": "0.2",
        "b": "45000.5",
        "B": "0.1",
        "a": "45001.5",
        "A": "0.1",
        "o": "44000.0",
        "h": "46000.0",
        "l": "43000.0",
        "v": "1000.0",
        "q": "45000000.0",
        "O": int(time.time() * 1000),
        "C": int(time.time() * 1000),
        "F": "100",
        "L": "200",
        "n": "150"
    })


@pytest.fixture
def data_processor():
    """
    Fixture to return an instance of the DataProcessor class.
    :return: DataProcessor: An instance of the DataProcessor class.
    """
    return DataProcessor("BTCUSDT")


if __name__ == "__main__":
    pytest.main()
