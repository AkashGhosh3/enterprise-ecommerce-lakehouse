from abc import ABC, abstractmethod


class BaseIngestion(ABC):

    @abstractmethod
    def extract(self):
        """Extract data from source"""
        pass

    @abstractmethod
    def save(self):
        """Save data to Bronze layer"""
        pass