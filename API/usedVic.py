from abc import ABC
from datetime import datetime

import requests
import re
from bs4 import BeautifulSoup

from API.unitInterface import UnitInterface

def digest_main_url(url: str, text=None) -> list:
    """
    Function to turn the given url into more usable data
    :param url: The URL to digest, this is the URL with all the listings, the main page
    :param text: For testing, your own HTML can be sent in instead
    """
    results = []
    if text is None:
        request_response = requests.get(url=url,
                                        headers={
                                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
                                        })
        response_text = request_response.text
    else:
        response_text = text

    soup = BeautifulSoup(response_text, "html.parser")
    print(soup)
    soup = soup.find("div",attrs={"class": "browse-ad-list"})
    listing = soup.find_all("a", attrs={"class": "ad-list-item-link"})
    for result in listing:
        try:
            tmp = url.split(".com")[0]
            url = tmp + ".com" + result.get("href")
            title_and_cost = result.text.strip().split(" · ")
            if len(title_and_cost) == 1:
                continue
            else:
                cost = title_and_cost[0]
                title = title_and_cost[1]

                cost = int(cost.replace("$","").replace(",",""))
                results += [Unit(url, title, cost)]
        except IndexError as e:
            print("Didn't match format: ", e, result)
        except ValueError as v:
            print("No Price: ", v, result)
    return results


class Unit(UnitInterface, ABC):
    """Important Elements to record
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
        assert type(bedrooms) is int or bedrooms is None
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

        self.__description = None

        self.__valid = True
        self.__time = datetime.now().timestamp()

        self.__website = "used vic"

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

    def digest_url(self, url: str = None, text: str = None) -> None:
        """
        Method to turn the given url into more usable data
        :param url: The URL to digest, this is the URL with the listing info, the unit page
        :param text: For testing, your own HTML can be sent in instead
        """
        try:
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
            self.__valid = False
            return
        soup = BeautifulSoup(response_text, "html.parser")
        list_items = soup.find_all("li", attrs={"class":"align-items-center"})
        for item in list_items:
            match = re.search("# of Bedrooms.*(\d).*", item.text)
            if match:
                self.__bedrooms = match.group(1)
            match = re.search("# of Bathrooms.*?(\d).*", item.text)
            if match:
                self.__bathrooms = match.group(1)
        description = soup.find("div", attrs={"class":"adview-ad-details"}).p.text.strip().split(" ")
        description = [word for word in description if word!=""]
        description = " ".join(description).replace("\n","").replace("\r","")
        self.__description = description

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