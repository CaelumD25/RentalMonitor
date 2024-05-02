import unittest

import requests

from API.kijiji import digest_main_url

class TestKijiji(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.main_url = "https://www.kijiji.ca/b-apartments-condos/victoria-bc/1+bedroom__1+bedroom+den__2+bedroom+den__2+bedrooms/c37l1700173a27949001?ll=48.462368%2C-123.313803&address=MacLaurin+Building%2C+Victoria%2C+BC+V8P+5C2%2C+Canada&radius=8.0&price=__2400"
        cls.main_text = "SampleHTML\\kijiji_main.html"
        cls.sub_text = "SampleHTML\\kijiji_sub.html"

    def test_full_case(self):
        results = digest_main_url(self.main_url)
        for result in results:
            result.digest_url()
            print(result)

    def test_first_3(self):
        count = 0
        results = digest_main_url(self.main_url)
        for result in results:
            result.digest_url()
            print(result)
            if count>=3:
                break
            count += 1

    def download(self):
        website = "kijiji"
        with open(self.main_text,"w", encoding='utf-8') as fp:
            result = requests.get(self.main_url).text
            fp.write(result)
        with open(self.sub_text,"w", encoding='utf-8') as fp:
            result = requests.get("https://www.kijiji.ca/v-apartments-condos/victoria-bc/1-bedroom-apartments-for-rent-in-victoria/1634176070").text
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
        results = digest_main_url(self.main_url,text=text)
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
            self.assertTrue(len(result.name)!=0 and type(result.name)==str)
            print(result.cost)
            self.assertTrue(result.cost<3000)
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