import datetime
from abc import ABC
import requests
import re
from bs4 import BeautifulSoup

from API.unitInterface import UnitInterface

def digest_main_url(url: str, text=None) -> list:
    """
    This function returns a list of Unit objects from the main page of craigslist
    :param url: The URL to digest, this is the URL with all the listings, the main page
    :param text: For testing, your own HTML can be sent in instead
    """
    results = []
    # Sets up the request response for the URL or text
    if text is None:
        request_response = requests.get(url=url,
                                        headers={
                                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
                                        })
        response_text = request_response.text
    else:
        response_text = text

    # Parse HTML with BeautifulSoup 4
    soup = BeautifulSoup(response_text, "html.parser")

    # Extract essential elements about each listing, this can then be further processed per unit with digest_url
    for elem in soup.find_all("li", attrs={"class": "cl-static-search-result"}):
        url = elem.find("a")["href"]
        name = elem.find("div", attrs={"class": "title"}).text.strip()
        cost = int(elem.find("div", attrs={"class":"price"}).text.replace("$","").replace(",","").strip())
        try:
            location = elem.find("div", attrs={"class":"location"}).text.strip()
        except AttributeError:
            location = None

        results += [Unit(url, name, cost, location=location)]
    return results


class Unit(UnitInterface, ABC):
    """
    Important Elements to record
    - Name
    - Cost
    - Bedrooms
    - Bathrooms
    - Bathrooms
    - Size
    - Location
    """

    def __init__(self, url: str, name: str = None, cost: int = None, bedrooms: int = None, bathrooms: int = None,
                size: int = None, location: str = None):
        assert type(url) is str
        self.__url = url

        # The Name of the listing
        assert type(name) is str or name is None
        self.__name = name

        # How much the unit costs in CAD
        assert type(cost) is int or cost is None
        self.__cost = cost

        # How many bedrooms in the unit
        assert type(bedrooms) is str or bedrooms is None
        self.__bedrooms = bedrooms

        # How many bathrooms in the unit
        assert type(bathrooms) is int or bathrooms is None
        self.__bathrooms = bathrooms

        # How large is the unit in squared units
        assert type(size) is int or size is None
        self.__size = size

        # Where is the unit located
        assert type(location) is str or location is None
        self.__location = location

        self.__valid = True
        self.__time = datetime.datetime.now().timestamp()

        self.description = None

    def __str__(self):
        return f"TITLE: {self.__name}\n" \
               f"URL: {self.__url}\n" \
               f"COST: {self.__cost}\n" \
               f"BEDROOMS: {self.__bedrooms}\n" \
               f"BATHROOMS: {self.__bathrooms}\n" \
               f"SIZE: {self.__size}\n" \
               f"LOCATION: {self.location}\n" \
               f"FOUND AT: {self.__time}\n" \
               f"DESCRIPTION: {self.__description}"

    def digest_url(self, url=None, text=None):
        """
        Method to turn the given url into more usable data
        :param url: The URL to digest, this is the URL with the listing info, the unit page
        :param text: For testing, your own HTML can be sent in instead
        """
        try:
            # Sets up the response HTML based on URL or text
            if text is None:
                if url is None:
                    request_response = requests.get(url=self.__url,
                                                    headers={
                                                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
                                                    })
                    response_text = request_response.text

                else:
                    request_response = requests.get(url=url,
                                                    headers={
                                                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
                                                    })
                    response_text = request_response.text
            else:
                response_text = text
        except requests.exceptions.RequestException:
            # If the URL is not valid, then the request fails and should be set to invalid
            self.__valid = False
            return

        # Process the rest of the data from the HTML
        soup = BeautifulSoup(response_text, "html.parser")
        info_section = soup.find("p", attrs={"class":"attrgroup"})
        info_section_text = info_section.text.lower().strip()

        matched = re.search(r".*(\d)br.*", info_section_text)
        if matched:
            self.__bedrooms = int(matched.group(1))
        matched = re.search(r".*(\d)ba.*", info_section_text)
        if matched:
            self.__bathrooms = int(matched.group(1))
        self.__description = soup.find("section",attrs={"id":"postingbody"}).text.strip().replace("\n","")

        self.__website = "craigslist"

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

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def time(self):
        return self.__time

    @property
    def website(self):
        return self.__website



