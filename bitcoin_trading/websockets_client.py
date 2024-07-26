"""
This module contains the BinanceWebSocket class which is responsible for connecting to the Binance WebSocket API and
receiving real-time data for a given symbol.
"""
import asyncio
import websockets
from bitcoin_trading.observer import BinanceSubject
from bitcoin_trading.utils import setup_logging

# Set up logging
logger = setup_logging()


class BinanceWebSocket:
    """
    Class to connect to the Binance WebSocket API and receive real-time data for a given symbol.
    """
    def __init__(self, symbol):
        """
        Constructor for the BinanceWebSocket class.
        :param symbol: str: The symbol to receive real-time
        data for, e.g. "btcusdt"
        :return: None
        """
        self.symbol = symbol
        self.uri = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
        self.subject = BinanceSubject()

    async def connect(self):
        """
        Connect to the Binance WebSocket API and receive real-time data.
        :return: None
        """
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    logger.info(f"WebSocket connection opened for {self.symbol}")
                    while True:
                        try:
                            message = await websocket.recv()
                            self.subject.notify(message)
                        except websockets.ConnectionClosed:
                            logger.warning("WebSocket connection closed unexpectedly")
                            break
            except Exception as e:
                logger.error(f"Error occurred: {e}")
                logger.info("Attempting to reconnect in 5 seconds...")
                await asyncio.sleep(5)
