import matplotlib.pyplot as plt
from datetime import datetime
from controller import close_soxs_values, close_soxl_values

class View:
    def display_graph(self, symbol, data, start_date_str, end_date_str):
        start_date = datetime.fromisoformat(start_date_str).replace(tzinfo=None)
        end_date = datetime.fromisoformat(end_date_str).replace(tzinfo=None)

        dates = []
        closes = []
        for date, values in data.items():
            date_obj = datetime.fromisoformat(date).replace(tzinfo=None)
            if start_date <= date_obj <= end_date:
                dates.append(date_obj)
                closes.append(values["Close"])

        plt.figure(figsize=(15, 10))
        plt.xticks(dates[::max(1, len(dates) // 10)], rotation=45)
        plt.plot(dates, closes, label=f'{symbol} Close Price')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title(f'Historical Close Price of {symbol}')
        plt.legend()
        plt.show()

    def print_account(self, account):
        print(f"\t---------Account Information---------")
        print(f"\tAccount balance: ${account.get_balance()}")
        print(f"\tSOXS shares: {account.soxs_shares}")
        print(f"\tSOXL shares: {account.soxl_shares}") 
        print(f"\tTotal account value: ${round(account.balance, 2) + int((account.soxs_shares * close_soxs_values[-1])) + int((account.soxl_shares * close_soxl_values[-1]))}")
        print(f"\t-------------------------------------")

def get_user_input():
    symbol = input("Enter the symbol (SOXS or SOXL): ").upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    return symbol, start_date, end_date