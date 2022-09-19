import requests
import re
from bs4 import BeautifulSoup
import time

from scrape_url import scrape

from API import kijiji as k
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Hello World")
    start_time = time
    for x in scrape("https://www.kijiji.ca/b-real-estate/victoria-bc/c34l1700173?address=MacLaurin+Building%2C+Victoria%2C+BC+V8P+5C2%2C+Canada&ll=48.462368,-123.313803"):
        print(x)
    print(time-start_time)
    #geolocator = bing.Bing("AkVuw-CNwasVEvDE8fqHd7qZ2YDO1UTxjkB9UEW7AfKWCJCJpKqInXb83YBH5EoI")
    #k.Unit().digest_url("https://www.kijiji.ca/v-apartments-condos/nelson/beasley-two-bedroom-apartment-with-a-view/1631541147?undefined", geolocator)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
