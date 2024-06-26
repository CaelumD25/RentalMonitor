from abc import ABC
from datetime import datetime
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
                                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
                                        })
        response_text = request_response.text
    else:
        response_text = text
    # Parse HTML with BeautifulSoup 4
    soup = BeautifulSoup(response_text, "html.parser")

    # Extract essential elements about each listing, this can then be further processed per unit with digest_url
    for elem in soup.find_all("div", attrs={"class": "search-item"}):
        try:
            name = elem.find("a", attrs={"class":"title"}).text.strip()
            url = "https://www.kijiji.ca" + elem.find("a", attrs={"class":"title"}).get("href")
            location = elem.find("div", attrs={"class":"location"}).span.text.strip()
            cost = elem.find("div", attrs={"class": "price"}).text.strip().split(".")[0]
            cost = int(cost.replace(",","").replace("$",""))
            bedrooms = elem.find("span", attrs={"class":"bedrooms"}).text.strip()
            match = re.search(r".*(\d).*", bedrooms)
            if match:
                bedrooms = int(match.group(1))
            else:
                bedrooms = None
            results += [Unit(url, name, cost, bedrooms, location=location)]
        except IndexError as e:
            print("Error scanning", e)
    return results


class Unit(UnitInterface, ABC):
    """Important Elements to record
    - Name
    - Cost
    - Bedrooms
    - Bathrooms
    - Bathrooms
    - Location
    """
    def __init__(self, url: str, name: str = None, cost: int = None, bedrooms: int = None,
                bathrooms: int = None, size: int = None, location: str = None):
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

        # Where is the unit located
        assert type(location) is str or location is None
        self.__location = location

        assert type(size) is int or size is None
        self.__size = size

        self.__description = None

        self.__valid = True
        self.__time = datetime.now().timestamp()

        self.__website = "kijiji"

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

        match = re.search(".*Bathrooms: (\d).*", soup.prettify())
        if match:
            self.__bathrooms = match.group(1)

        attribute_results = soup.select('[class^="twoLinesAttribute-"]')
        for result in attribute_results:
            match = re.search("Size \(sqft\).*?(\d+)",result.text.replace(",",""))
            if match:
                self.__size = match.group(1)
        try:
            description_result = soup.select_one('[class^="descriptionContainer-"]').p.text.replace("\n","")
            self.__description = description_result
        except AttributeError:
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
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: str):
        self.__size = value

    @property
    def time(self):
        return self.__time

    @property
    def website(self):
        return self.__website