import unittest
from API.craigslist import digest_main_url
class TestCraigsList(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.main_url = "https://victoria.craigslist.org/search/victoria-bc/apa?lat=48.4668&lon=-123.3112&max_price=1600&search_distance=2.5&sort=date#search=1~thumb~0~4"

    def test_full_case(self):
        results = digest_main_url(self.main_url)
        for result in results:
            result.digest_url()
            print(result)

    def test_static_first_case(self):
        text = ""
        with open("SampleHTML\craigslist_html_example.html") as fp:
            text = fp.read()
        result = digest_main_url(self.main_url, text=text)[0]
        print(result)

    def test_first_with_digest_case(self):
        text = ""
        with open("SampleHTML\craigslist_html_example.html") as fp:
            text = fp.read()
        results = digest_main_url(self.main_url,text=text)
        results[0].digest_url()
        print(results[0])

    def test_old_data_case(self):
        text = ""
        with open("SampleHTML\craigslist_html_example.html") as fp:
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