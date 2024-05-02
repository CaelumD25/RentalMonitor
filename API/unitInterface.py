from abc import ABC, abstractmethod

class UnitInterface(ABC):
    @abstractmethod
    def __init__(self, url: str, name: str = None, cost: int = None, bedrooms: int = None, bathrooms: int = None,
                size: str = None, location: str = None) -> None:
        self.__website = None
        self.__time = None
        self.__description = None

    @abstractmethod
    def digest_url(self, url: str = None, text: str = None) -> None:
        """
        Class to turn the given url into more usable data
        :param url: The URL to digest, this is the URL with all the listings, the main page
        :param text: For testing, your own HTML can be sent in instead
        """
        pass

    @abstractmethod
    def __str__(self) -> None:
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def cost(self) -> int:
        pass

    @cost.setter
    @abstractmethod
    def cost(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def bedrooms(self) -> int:
        pass

    @bedrooms.setter
    @abstractmethod
    def bedrooms(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def bathrooms(self) -> int:
        pass

    @bathrooms.setter
    @abstractmethod
    def bathrooms(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @size.setter
    @abstractmethod
    def size(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def location(self) -> str:
        pass

    @location.setter
    @abstractmethod
    def location(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def time(self):
        pass

    @property
    @abstractmethod
    def website(self):
        pass