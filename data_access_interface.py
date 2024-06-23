import database as db

class DataAccessInterface(db.DataBase):
    data = None

    def __init__(self, database):
        self.data = database

    def download_data(self):
        self.data.download_data()

    def load_data(self):
        return self.data.load_data()