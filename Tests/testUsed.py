import unittest
from API.usedVic import digest_main_url
import requests
class TestUsed(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.main_url = "https://www.usedvictoria.com/apartment-rentals?lat=48.46745824148332&lon=-123.32977294921876&ca=%7B%227%22%3A%5B%222%22,null%5D,%228%22%3A%5B%221%22,null%5D%7D&radius=5&priceTo=2400&xflags=wanted"
        cls.main_text = "SampleHTML\\used_main.html"
        cls.sub_text = "SampleHTML\\used_sub.html"

    def test_full_case(self):
        results = digest_main_url(self.main_url)
        for result in results:
            result.digest_url()
            print(result)
            print("*"*20)

    def test_first_3(self):
        count = 0
        results = digest_main_url(self.main_url)
        for result in results:
            result.digest_url()
            print(result)
            print("*" * 20)
            if count >= 3:
                break
            count += 1

    def download(self):
        website = "kijiji"
        with open(self.main_text, "w", encoding='utf-8') as fp:
            result = requests.get(self.main_url).text
            fp.write(result)
        with open(self.sub_text, "w", encoding='utf-8') as fp:
            result = requests.get(
                "https://www.usedvictoria.com/apartment-rentals/40211323").text
            fp.write(result)

    def test_static_first_case(self):
        text = ""
        with open(self.main_text, encoding='utf-8') as fp:
            text = fp.read()
        result = digest_main_url(self.main_url, text=text)[0]
        print(result)

    def test_first_with_digest_case(self):
        text = ""
        with open(self.main_text, encoding='utf-8') as fp:
            text = fp.read()
        results = digest_main_url(self.main_url, text=text)
        results[0].digest_url()
        print(results[0])

    def test_old_data_case(self):
        text = ""
        with open(self.main_text) as fp:
            text = fp.read()
        results = digest_main_url(self.main_url, text=text)
        for result in results:
            result.digest_url()
            print(result)

    def test_with_stored_html(self):
        text = ""
        with open("SampleHTML\craigslist_html_example.html") as fp:
            text = fp.read()
        results = digest_main_url(url=self.main_url, text=text)
        for result in results:
            print(result.url)
            self.assertTrue("https" in result.url)
            print(result.name)
            self.assertTrue(len(result.name) != 0 and type(result.name) == str)
            print(result.cost)
            self.assertTrue(result.cost < 3000)
            print(result.location)

    def test_with_stored_html_digest_individual_html(self):
        text = ""
        with open("SampleHTML\craigslist_html_example.html") as fp:
            text = fp.read()
        results = digest_main_url(url=self.main_url, text=text)
        result = results[0]
        inside_text = ""
        with open("SampleHTML\craigslist_listing_html.html") as fp:
            inside_text = fp.read()
        result.digest_url(text=inside_text)
        print(result)
        self.assertTrue(result.bedrooms != 0)
        self.assertTrue(result.bathrooms != 0)