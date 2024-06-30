import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import json
import csv
import os
from abc import ABC, abstractmethod

class Publisher:
    def __init__(self):
        self.subscribers = []
        self.data = None

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update(self.data)

    def update_data(self, new_data):
        self.data = new_data
        self.notify()

class Subscriber(ABC):
    @abstractmethod
    def update(self, data):
        pass

class GraphSubscriber(Subscriber):
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = datetime.datetime.fromisoformat(start_date).replace(tzinfo=None)  # Ensure these are naive datetime objects
        self.end_date = datetime.datetime.fromisoformat(end_date).replace(tzinfo=None)

    def update(self, data):
        self.display_graph(data)

    def display_graph(self, data):
        if self.symbol == "SOXS":
            symbol_data = data["SOXS"]
        else:
            symbol_data = data["SOXL"]

        dates = []
        closes = []

        for date, values in symbol_data.items():
            date_obj = datetime.datetime.fromisoformat(date).replace(tzinfo=None)  # Convert to naive datetime object
            if self.start_date <= date_obj <= self.end_date:  # Compare naive datetime objects
                dates.append(date_obj)
                closes.append(values["Close"])

        if not dates:
            print(f"No data available for {self.symbol} between {self.start_date} and {self.end_date}")
            return

        tick_frequency = max(1, len(dates) // 10)
        plt.figure(figsize=(15, 10))
        plt.xticks(dates[::tick_frequency], rotation=45)
        plt.plot(dates, closes, label=f'{self.symbol} Close Price')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'Historical Close Price of {self.symbol}')
        plt.legend()
        plt.show()

def download_data():
    soxs_ticker = yf.Ticker('SOXS') 
    soxl_ticker = yf.Ticker('SOXL')

    soxs_hist = soxs_ticker.history(start="2021-01-01", end=None, interval="1d", actions=False)
    soxl_hist = soxl_ticker.history(start="2021-01-01", end=None, interval="1d", actions=False)

    soxs_data_dict = {str(date): data for date, data in soxs_hist.to_dict(orient="index").items()}
    soxl_data_dict = {str(date): data for date, data in soxl_hist.to_dict(orient="index").items()}

    soxs_file_name = "soxs_historical_data.json"
    soxl_file_name = "soxl_historical_data.json"

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
        return {"SOXS": soxs_data, "SOXL": soxl_data}
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None


def get_user_input():
    symbol = input("Enter the symbol (SOXS or SOXL): ").upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    return symbol, start_date, end_date

def main():
    download_data()

    publisher = Publisher()

    symbol, start_date, end_date = get_user_input()
    graph_subscriber = GraphSubscriber(symbol, start_date, end_date)
    publisher.subscribe(graph_subscriber)

    new_data = load_data()
    if new_data:
        publisher.update_data(new_data)

if __name__ == "__main__":
    main()