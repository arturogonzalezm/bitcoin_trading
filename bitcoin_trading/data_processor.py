"""
This module is responsible for processing the data received from the Binance API.
"""
import json
import time
from datetime import datetime
import polars as pl
import os
from bitcoin_trading.observer import Observer
from bitcoin_trading.utils import setup_logging

# Set up logging
logger = setup_logging()


class DataProcessor(Observer):
    """
    Class to process the data received from the Binance API.
    """
    def __init__(self, symbol):
        """
        Constructor for the DataProcessor class.
        :param symbol: str: The symbol to process the data for, e.g. "btcusdt"
        :return: None
        """
        self.df = pl.DataFrame()
        self.symbol = symbol

    def update(self, message):
        """
        Process the data received from the Binance API.
        :param message: str: The message received from the Binance API
        :return: None
        """
        data = json.loads(message)
        current_time = int(time.time() * 1000)
        latency = current_time - int(data['E'])

        formatted_data = {
            "Event Time": [datetime.fromtimestamp(int(data['E']) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')],
            "Symbol": [data['s']],
            "Price Change": [float(data['p'])],
            "Price Change Percent": [float(data['P'])],
            "Weighted Average Price": [float(data['w'])],
            "First Trade Price": [float(data['x'])],
            "Last Price": [float(data['c'])],
            "Last Quantity": [float(data['Q'])],
            "Best Bid Price": [float(data['b'])],
            "Best Bid Quantity": [float(data['B'])],
            "Best Ask Price": [float(data['a'])],
            "Best Ask Quantity": [float(data['A'])],
            "Open Price": [float(data['o'])],
            "High Price": [float(data['h'])],
            "Low Price": [float(data['l'])],
            "Total Traded Base Asset Volume": [float(data['v'])],
            "Total Traded Quote Asset Volume": [float(data['q'])],
            "Statistics Open Time": [datetime.fromtimestamp(int(data['O']) / 1000).strftime('%Y-%m-%d %H:%M:%S')],
            "Statistics Close Time": [datetime.fromtimestamp(int(data['C']) / 1000).strftime('%Y-%m-%d %H:%M:%S')],
            "First Trade ID": [int(data['F'])],
            "Last Trade ID": [int(data['L'])],
            "Total Number of Trades": [int(data['n'])],
            "Latency": [latency]
        }

        new_row = pl.DataFrame(formatted_data)
        self.df = pl.concat([self.df, new_row])
        logger.info(f"New data processed: {new_row}")

        if len(self.df) % 10 == 0:
            logger.info("Calling save_to_csv")
            self.save_to_csv()

    def save_to_csv(self):
        """
        Save the processed data to a CSV file.
        :return: None
        """
        os.makedirs('data', exist_ok=True)
        filename = f'data/binance_{self.symbol}_data.csv'
        self.df.write_csv(filename)
        logger.info(f"Data saved to {filename}")
