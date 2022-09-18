import requests
import re
from bs4 import BeautifulSoup
from geopy.geocoders import bing

class Unit:
    """Important Elements to record
    - Name
    - Cost
    - Bedrooms
    - Bathrooms
    - Bathrooms
    - Location
    """
    def __int__(self, url: str, geolocator: bing, name: str = None, cost: int = None, bedrooms: int = None,
                bathrooms: int = None, location: str = None):
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

        # Where is the unit located
        assert type(location) is str or None
        self.__location = location

        self.__description = None

        self.digest_url(self.__url, geolocator)

    def digest_url(self, url, geolocator):
        """method to turn the given url into the usable data"""
        requested_html = requests.get(url).text
        soup = BeautifulSoup(requested_html, "html.parser")
        info_div = soup.select("#ViewItemPage")[0]

        # Name
        name_div = info_div.select('h1[class^="title-"]')[0]
        self.__name = name_div.text

        # Cost
        price_div = info_div.select('div[class^="priceWrapper"]')[0]
        cost = price_div.select("span")[0].text
        self.__cost = int(cost.replace(",", "").replace("$", ""))

        # Bedrooms and Bathrooms
        value_label_div = info_div.select('span[class^="noLabelValue-"]')
        for item in value_label_div:
            if "Bedroom" in item.text:
                self.__bedrooms = int(re.search(r"\w*(\d+)", item.text).group(1))
            elif "Bathroom" in item.text:
                self.__bathrooms = int(re.search(r"\w*(\d+)", item.text).group(1))

        # Location
        location_div = info_div.select('span[itemprop^="address"]')[0]
        location = location_div.text
        location_result = geolocator.geocode(location)
        self.__location = location_result
        print()

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
    def location(self):
        return self.__location

    @location.setter
    def location(self, value: str):
        self.__location = value