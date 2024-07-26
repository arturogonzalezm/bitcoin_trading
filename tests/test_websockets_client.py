"""
Tests for BinanceWebSocket class which connects to the Binance WebSocket API and receives real-time data.
"""

import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import pytest
import websockets
from bitcoin_trading.observer import BinanceSubject
from bitcoin_trading.websockets_client import BinanceWebSocket


@pytest.fixture
def caplog_fixture(caplog):
    """
    Fixture for capturing log output.
    """
    return caplog


@pytest.fixture
def binance_websocket_fixture():
    """
    Fixture for initializing BinanceWebSocket with the symbol 'btcusdt'.
    """
    return BinanceWebSocket("btcusdt")


@pytest.mark.asyncio
async def test_binance_websocket_initialization(binance_websocket_fixture):
    """
    Test the initialization of BinanceWebSocket.
    :param binance_websocket_fixture: Fixture for BinanceWebSocket.
    """
    assert binance_websocket_fixture.symbol == "btcusdt"
    assert binance_websocket_fixture.uri == "wss://stream.binance.com:9443/ws/btcusdt@ticker"
    assert isinstance(binance_websocket_fixture.subject, BinanceSubject)


def message_generator(max_messages=10):
    """
    Generator function to simulate WebSocket messages and connection closure.
    :param max_messages: int: The number of messages to generate before closing the connection.
    """
    for _ in range(max_messages):
        yield "message"
    yield websockets.ConnectionClosed(1000, "normal closure")


if __name__ == "__main__":
    pytest.main()
