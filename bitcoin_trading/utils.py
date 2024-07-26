"""
This module contains utility functions that are used throughout the project.
"""
import logging


def setup_logging():
    """
    Setup logging configuration.
    :return: logger
    :rtype: logging.Logger
    """
    logger = logging.getLogger('bitcoin_trading.utils')

    # Check if the logger already has handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    return logger
