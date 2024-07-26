"""
Observer pattern implementation
"""
from abc import ABC, abstractmethod

from bitcoin_trading.utils import setup_logging

# Set up logging
logger = setup_logging()


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """
    @abstractmethod
    def attach(self, observer):
        """
        Attach an observer to the subject.
        :param observer: Observer
        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def detach(self, observer):
        """
        Detach an observer from the subject.
        :param observer: Observer
        :return: None
        """
        pass

    @abstractmethod
    def notify(self, message):
        """
        Notify all observers about an event.
        :param message: str
        :return: None
        """
        pass


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """
    @abstractmethod
    def update(self, message):
        """
        Receive update from subject.
        :param message: str
        :return: None
        """
        pass


class BinanceSubject(Subject):
    """
    Concrete Subject class that implements the Subject interface.
    """
    def __init__(self):
        """
        Initialize the list of observers.
        """
        self._observers = []

    def attach(self, observer):
        """
        Attach an observer to the subject.
        :param observer: Observer
        :return: None
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info("Observer %s attached", observer)
        else:
            logger.info("Observer %s already attached", observer)

    def detach(self, observer):
        """
        Detach an observer from the subject.
        :param observer: Observer
        :return: None
        """
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info("Observer %s detached", observer)
        else:
            logger.warning("Observer %s not found, could not detach", observer)

    def notify(self, message):
        """
        Notify all observers about an event.
        :param message: str
        :return: None
        """
        for observer in self._observers:
            observer.update(message)
