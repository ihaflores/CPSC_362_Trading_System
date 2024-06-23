import database as db

class DataAccessInterface(db.DataBase):
    database = None

    def __init__(self, database):
        self.database = database

    def download_data(self):
        self.database.download_data()

    def load_data(self):
        return self.database.load_data()