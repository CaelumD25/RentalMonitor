import requests
import re
from bs4 import BeautifulSoup


class Unit:
    """Important Elements to record
    - Name
    - Cost
    - Bedrooms
    - Bathrooms
    - Bathrooms
    - Size
    - Location
    """

    def __int__(self, url: str, name: str = None, cost: int = None, bedrooms: int = None, bathrooms: int = None,
                size: str = None, location: str = None):
        assert type(url) is str
        self.__url = url

        # The Name of the listing
        assert type(name) is str or None
        self.__name = name

        # How much the unit costs in CAD
        assert type(cost) is str or None
        self.__cost = cost

        # How many bedrooms in the unit
        assert type(bedrooms) is str or None
        self.__bedrooms = bedrooms

        # How many bathrooms in the unit
        assert type(bathrooms) is str or None
        self.__bathrooms = bathrooms

        # How large is the unit in squared units
        assert type(size) is str or None
        self.__size = size

        # Where is the unit located
        assert type(location) is str or None
        self.__location = location

    def digest_url(self, url):
        """class to turn the given url into the usable data"""
        pass

    @property
    def url(self):
        return self.__url

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, value: int):
        self.__cost = value

    @property
    def bedrooms(self):
        return self.__bedrooms

    @bedrooms.setter
    def bedrooms(self, value: int):
        self.__bedrooms = value

    @property
    def bathrooms(self):
        return self.__bathrooms

    @bathrooms.setter
    def bathrooms(self, value: int):
        self.__bathrooms = value

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: str):
        self.__size = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value: str):
        self.__location = value

