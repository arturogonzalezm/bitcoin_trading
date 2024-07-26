"""
This module contains the BinanceWebSocket class which is responsible for connecting to the Binance WebSocket API and
receiving real-time data for a given symbol.
"""
import asyncio
import websockets
from bitcoin_trading.observer import BinanceSubject
from bitcoin_trading.utils import setup_logging
from bitcoin_trading.config import WS_URI_TEMPLATE

# Set up logging
logger = setup_logging()


class BinanceWebSocket:
    """
    Class to connect to the Binance WebSocket API and receive real-time data for a given symbol.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, symbol):
        """
        Constructor for the BinanceWebSocket class.
        :param symbol: str: The symbol to receive real-time
        data for, e.g. "btcusdt"
        :return: None
        """
        self.symbol = symbol
        self.uri = WS_URI_TEMPLATE.format(symbol=symbol)
        self.subject = BinanceSubject()

    async def connect(self):
        """
        Connect to the Binance WebSocket API and receive real-time data.
        :return: None
        """
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    logger.info("WebSocket connection opened for %s", self.symbol)
                    while True:
                        try:
                            message = await websocket.recv()
                            self.subject.notify(message)
                        except websockets.ConnectionClosed:
                            logger.warning("WebSocket connection closed unexpectedly")
                            break
            except (websockets.WebSocketException, ConnectionError) as e:
                logger.error("Error occurred: %s", e)
                logger.info("Attempting to reconnect in 5 seconds...")
                await asyncio.sleep(5)
