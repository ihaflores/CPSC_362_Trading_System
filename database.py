import json
import yfinance as yf

class Target:
    def download_data(self):
        pass
    def load_data(self):
        pass    

class DataAccessAdapter(Target):
    def __init__(self, database):
        self.database = database

    def download_data(self):
        self.database.download_data()

    def load_data(self):
        return self.database.load_data()

class DataBase:

    # Stock data
    soxs_data = None
    soxl_data = None

    def __init__(self):
        pass

    def download_data(self):
        # Set the tickers for the SOXS and SOXL stocks
        soxs_ticker = yf.Ticker('SOXS') 
        soxl_ticker = yf.Ticker('SOXL')

        # Download historical data
        soxs_hist = soxs_ticker.history(start="2021-01-01", end=None, interval="1d", actions = False)
        soxl_hist = soxl_ticker.history(start="2021-01-01", end=None, interval="1d", actions = False)

        # Save historical data to JSON files
        soxs_data_dict = {str(date): data for date, data in soxs_hist.to_dict(orient="index").items()}
        soxl_data_dict = {str(date): data for date, data in soxl_hist.to_dict(orient="index").items()}

        # Set the file names for the JSON files
        soxs_file_name = "soxs_historical_data.json"
        soxl_file_name = "soxl_historical_data.json"

        # Save the data to JSON files
        with open(soxs_file_name, "w") as json_file:
            json.dump(soxs_data_dict, json_file, indent=4)

        with open(soxl_file_name, "w") as json_file:
            json.dump(soxl_data_dict, json_file, indent=4)

        print(f"Historical data for SOXS has been saved to {soxs_file_name}")
        print(f"Historical data for SOXL has been saved to {soxl_file_name}")

    def load_data(self):
        try:
            with open('soxs_historical_data.json') as self.fs, open('soxl_historical_data.json') as self.fl: 
                self.soxs_data = json.load(self.fs)
                self.soxl_data = json.load(self.fl)
            return self.soxs_data, self.soxl_data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None