import unittest
import os
import database as db
from database import DataBase

class TestDatabase(unittest.TestCase):
    def test_download_data(self):
        db = DataBase()
        db.download_data()
        self.assertTrue(os.path.exists("soxs_historical_data.json"))
        self.assertTrue(os.path.exists("soxl_historical_data.json"))

    def test_load_data(self):
        db = DataBase()
        db.download_data()
        soxs_data, soxl_data = db.load_data()
        self.assertTrue(soxs_data is not None)
        self.assertTrue(soxl_data is not None)

if __name__ == '__main__':
    unittest.main()