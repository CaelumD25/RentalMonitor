import unittest

from Database.sqlDatabase import SQL
from API.craigslist import Unit
class MyTestCase(unittest.TestCase):
    def test_value_in_db(self):
        new_unit = Unit("https://victoria.craigslist.org/apa/d/victoria-above-ground-bedroom-suite/7638827632.html","Above ground 1 bedroom suite near Uvic")
        db = SQL("C:/Users/caelu/PycharmProjects/RentalMonitor/Database/Rentals.db")
        self.assertTrue(db.unit_exists(new_unit))

    def test_value_not_in_db(self):
        new_unit = Unit("https://victoria.craigslist.org/apa/d/victoria-above-ground-bedroom-suite/7638827632.html","Above grobedroom suite near Uvic")
        db = SQL("C:/Users/caelu/PycharmProjects/RentalMonitor/Database/Rentals.db")
        self.assertFalse(db.unit_exists(new_unit))


if __name__ == '__main__':
    unittest.main()
