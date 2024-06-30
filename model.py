import yfinance as yf
import json

close_soxs_values = []
close_soxl_values = []

class Account:
    balance = 0
    initial_balance = 0
    soxs_shares = 0
    soxl_shares = 0
    running_soxs_spent = 0
    running_soxl_spent = 0

    def __init__(self, balance=100000):
        self.balance = balance
        self.initial_balance = balance

    def get_balance(self):
        return round(self.balance, 2)
    
    def get_initial_balance(self):
        return round(self.initial_balance, 2)
    
    def get_shares(self, stock):
        return self.soxs_shares if stock == "SOXS" else self.soxl_shares
    
    def get_running_stock_balance(self, stock):
        return self.running_soxs_spent if stock == "SOXS" else self.running_soxl_spent
    
    def get_portfolio_value(self):
        return self.balance + (self.soxs_shares * close_soxs_values[-1]) + (self.soxl_shares * close_soxl_values[-1])
    
    def calc_account_return(self):
        return round(((self.get_portfolio_value() - self.initial_balance) / self.initial_balance) * 100, 2)

    def buy_stock(self, stock, no_of_shares, price):
        spent = int(price) * int(no_of_shares)
        if stock == "SOXS":
            self.soxs_shares += no_of_shares
            self.running_soxs_spent += spent
        elif stock == "SOXL":
            self.soxl_shares += no_of_shares
            self.running_soxl_spent += spent
        self.balance -= spent
    
    def sell_stock(self, stock, no_of_shares, price):
        spent = round(price * no_of_shares, 2)
        if stock == "SOXS":
            self.soxs_shares -= no_of_shares
            self.running_soxs_spent -= spent
        elif stock == "SOXL":
            self.soxl_shares -= no_of_shares
            self.running_soxl_spent -= spent
        self.balance += spent

def download_data():
    soxs_ticker = yf.Ticker('SOXS')
    soxl_ticker = yf.Ticker('SOXL')
    soxs_hist = soxs_ticker.history(start="2021-01-01", end=None, interval="1d", actions=False)
    soxl_hist = soxl_ticker.history(start="2021-01-01", end=None, interval="1d", actions=False)
    soxs_data_dict = {str(date): data for date, data in soxs_hist.to_dict(orient="index").items()}
    soxl_data_dict = {str(date): data for date, data in soxl_hist.to_dict(orient="index").items()}
    with open("soxs_historical_data.json", "w") as json_file:
        json.dump(soxs_data_dict, json_file, indent=4)
    with open("soxl_historical_data.json", "w") as json_file:
        json.dump(soxl_data_dict, json_file, indent=4)

def load_data():
    try:
        with open('soxs_historical_data.json') as fs, open('soxl_historical_data.json') as fl:
            soxs_data = json.load(fs)
            soxl_data = json.load(fl)
        return soxs_data, soxl_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def calc_sma(symbol, data, period):
    sma = 0
    close_values = close_soxs_values if symbol == 'SOXS' else close_soxl_values
    close_values.append(data['Close'])
    if len(close_values) < period:
        return None
    for i in close_values[-period:]:
        sma += i
    sma = sma / period
    return sma

def calc_gain_loss(price, purchase_price):
    return round(((price - purchase_price) / purchase_price) * 100, 2)
