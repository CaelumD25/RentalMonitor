import re
from bs4 import BeautifulSoup
import requests

def match_url(url):
    if re.match(url, r"(https://www\.kijiji\.ca).*"):
        print("Kijiji Found")
        return 1
    elif re.match(url, r"https://.*?\.(craigslist.org).*"):
        print("Craigslist Found")
        return 2
    elif re.match(url, r"(https://www\.usedvictoria\.com/).*"):
        print("Used Victoria Found")
        return 3
    elif re.match(url, r""):
        print("Facebook Found")
        return 4
    else:
        return 5


def scrape_kijiji(url):
    requested_html = requests.get(url).text
    soup = BeautifulSoup()
    pass


def scrape_craigslist(url):
    pass


def scrape_used_vic(url):
    pass


def scrape_fb(url):
    pass


def scrape(url: str):
    match match_url(url):
        case 1:
            scrape_kijiji(url)
        case 2:
            scrape_craigslist(url)
        case 3:
            scrape_used_vic(url)
        case 4:
            scrape_fb(url)
        case 5:
            print("An error occurred in determine which website to scrape")