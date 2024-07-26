"""
Main module to run the application.
"""
import asyncio
from bitcoin_trading.websockets_client import BinanceWebSocket
from bitcoin_trading.data_processor import DataProcessor


async def main():
    """
    Main function to run the application.
    :return: None
    """
    symbol = "btcusdt"
    binance_ws = BinanceWebSocket(symbol)
    data_processor = DataProcessor(symbol)
    binance_ws.subject.attach(data_processor)
    await binance_ws.connect()


if __name__ == "__main__":
    asyncio.run(main())
