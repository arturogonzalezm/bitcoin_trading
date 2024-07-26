import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import websockets
from websockets import ConnectionClosed

from bitcoin_trading.observer import BinanceSubject
from bitcoin_trading.websockets_client import BinanceWebSocket


@pytest.fixture
def caplog(caplog):
    return caplog


@pytest.fixture
def binance_websocket():
    return BinanceWebSocket("btcusdt")


@pytest.mark.asyncio
async def test_binance_websocket_initialization(binance_websocket):
    assert binance_websocket.symbol == "btcusdt"
    assert binance_websocket.uri == "wss://stream.binance.com:9443/ws/btcusdt@ticker"
    assert isinstance(binance_websocket.subject, BinanceSubject)


@pytest.mark.asyncio
async def test_connect_successful_connection(binance_websocket, caplog):
    mock_websocket = AsyncMock()
    mock_websocket.__aenter__.return_value = mock_websocket
    mock_websocket.recv.side_effect = ["message1", "message2", websockets.ConnectionClosed(None, None)]

    # Mock the notify method of the subject
    binance_websocket.subject.notify = MagicMock()

    with patch('websockets.connect', return_value=mock_websocket):
        try:
            await asyncio.wait_for(binance_websocket.connect(), timeout=0.1)
        except asyncio.TimeoutError:
            pass  # Expected behavior, as the method will keep trying to reconnect

    assert "WebSocket connection opened for btcusdt" in caplog.text
    assert "WebSocket connection closed unexpectedly" in caplog.text
    binance_websocket.subject.notify.assert_any_call("message1")
    binance_websocket.subject.notify.assert_any_call("message2")


if __name__ == "__main__":
    pytest.main()
