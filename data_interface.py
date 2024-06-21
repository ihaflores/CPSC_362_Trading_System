import json
import yfinance as yf

def open_JSON_files():
    try:
        fs = open('soxs_historical_data.json')
        fl = open('soxl_historical_data.json')
        return fs, fl
    except Exception as e:
        print(f"Error opening JSON files: {e}")
        return None, None
    
def close_JSON_files(fs, fl):
    try:
        fs.close()
        fl.close()
    except Exception as e:
        print(f"Error closing JSON files: {e}")

def download_data():
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

def load_data():
    try:
        with open('soxs_historical_data.json') as fs, open('soxl_historical_data.json') as fl:
            soxs_data = json.load(fs)
            soxl_data = json.load(fl)
        return soxs_data, soxl_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None