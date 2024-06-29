import yfinance as yf
import json
import ui
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os


close_soxs_values = []
close_soxl_values = []

class Account:
    balance = 0
    initial_balance = 0
    soxs_shares = 0
    soxl_shares = 0
    running_soxs_spent = 0
    running_soxl_spent = 0

    def __init__(self, balance = 100000):
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
        # Calculate the account return percentage
        return round(((self.get_portfolio_value() - self.initial_balance) / self.initial_balance) * 100, 2)

    def buy_stock(self, stock, no_of_shares, price):
        spent = int(price) * int(no_of_shares)

        print(f"Buying {no_of_shares} shares of {stock} at ${price} each for a total ${spent}.\nAccount balance before: ${self.balance}")
        
        if stock == "SOXS":
            self.soxs_shares += no_of_shares
            self.running_soxs_spent += spent
        elif stock == "SOXL":
            self.soxl_shares += no_of_shares
            self.running_soxl_spent += spent
        self.balance -= spent
        round(self.balance, 2)
        print(f"Account balance after: ${round(self.balance, 2)}")
    
    def sell_stock(self, stock, no_of_shares, price):
        spent = round(price * no_of_shares, 2)

        print(f"Selling {no_of_shares} shares of {stock} at ${price} each for a total ${spent}.\nAccount balance before: ${self.balance}")
        if stock == "SOXS":
            self.soxs_shares -= no_of_shares
            self.running_soxs_spent -= spent
        elif stock == "SOXL":
            self.soxl_shares -= no_of_shares
            self.running_soxl_spent -= spent
        self.balance += spent
        round(self.balance, 2)
        print(f"Account balance after: ${self.balance}")

    def print_account(self):
        print(f"\t---------Account Information---------")
        print(f"\tAccount balance: ${self.balance}")
        print(f"\tSOXS shares: {self.soxs_shares}")
        print(f"\tSOXL shares: {self.soxl_shares}") 
        print(f"\tTotal account value: ${round(self.balance, 2) + int((self.soxs_shares * close_soxs_values[-1])) + int((self.soxl_shares * close_soxl_values[-1]))}")
        print(f"\t-------------------------------------")

# Writes a row to the output CSV file
# Columns: Date, Stock, Trade, No. of Shares, Price, Gain/Loss, Balance
def write_data_to_csv(data):
    with open('trades.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()

def initialize_csv_file():
    # Check if CSV file exists and delete it
    if os.path.exists("trades.csv"):
        os.remove("trades.csv")

    # Write first row to CSV file
    write_data_to_csv(['Date', 'Stock', 'Trade', 'No. of Shares', 'Price', 'Gain/Loss', '% Return', 'Balance'])

def write_final_summary_to_csv(account):
    # Write the summary lines to the CSV file (also print to console)
    write_data_to_csv(["Portfolio Lifetime Summary:"])
    write_data_to_csv(["Total Gain/Loss", "Total % Return", "Final Balance", "Final Portfolio Value"])
    print("\nPortfolio Lifetime Summary:")

    # Calculate the total gain/loss and total account return
    total_gain_loss = round(account.get_portfolio_value() - account.get_initial_balance(), 2)
    total_account_return = account.calc_account_return()

    # Write the summary data to the CSV file (also print to console)
    write_data_to_csv([total_gain_loss,total_account_return,account.get_balance(), round(account.get_portfolio_value(), 2)])
    print(f"Total Gain/Loss = ${total_gain_loss}, Total % Return = {total_account_return}%, Final Balance = ${account.get_balance()}, Final Portfolio Value = ${account.get_portfolio_value()}")

def write_trade_to_csv(trade, account, soxs, soxl):
    # Get the trade data
    symbol = trade[1]
    buy_sell = trade[0]
    no_of_shares = int(trade[2])

    if symbol == "SOXS":
        date = get_date(soxs)
        close_value = close_soxs_values[-1]
    else:
        date = get_date(soxl)
        close_value = close_soxl_values[-1]

    # Calculate gain/loss and % return
    todays_return = account.calc_account_return()
    gain_loss = calc_gain_loss(close_value, (account.get_running_stock_balance(symbol)/no_of_shares)) if buy_sell == "Sell" else 0

    # Write the trade data to CSV file
    write_data_to_csv([date, symbol, buy_sell, no_of_shares, round(close_value, 2), gain_loss, todays_return, account.get_balance()])

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

def get_date(data):
    # Return the date of the stock information
    return data[0]

def get_data(data):
    # Return the data of the stock information
    return data[1]

def calc_sma(symbol, data, period):
    # Initialize the simple moving average
    sma = 0

    # Select the stock
    close_values = close_soxs_values if symbol == 'SOXS' else close_soxl_values

    # Append the close value to the list
    close_values.append(get_data(data)['Close'])
    
    # Check if enough data has been collected to calculate the SMA
    if len(close_values) < period:
        print(f'\tNot enough data for {symbol} to calculate SMA')
        return None
    
    # Calculate the total value by iterating through the last 10 values
    for i in close_values[-period:]:
        sma += i

    # Calculate the average by dividing the total value by the period
    sma = sma / period

    # Return the simple moving average
    print(f'\t{symbol} SMA: ' + str(sma))
    return sma

def calc_gain_loss(price, purchase_price):
    # Calculate the gain/loss percentage on a sell
    return round(((price - purchase_price) / purchase_price) * 100, 2)

def EvaluateSMA(soxs_sma, soxl_sma, account):
    # Get the balance and holdings
    balance = account.get_balance()
    no_soxs_shares = account.get_shares("SOXS")
    no_soxl_shares = account.get_shares("SOXL")

    # Rename close values for readability
    # prev_soxs_close = close_soxs_values[-2]
    # prev_soxl_close = close_soxl_values[-2]
    soxs_close = close_soxs_values[-1]
    soxl_close = close_soxl_values[-1]

    # Initialize the trades list
    trades = []

    # Initialize the signals
    signal_soxl = False
    signal_soxs = False

    # Calculate the number of shares to buy
    soxs_buy = (balance * 0.1) // soxs_close
    soxl_buy = (balance * 0.05) // soxl_close

    # Determine what symbol we are trading
    if soxs_sma > soxl_sma:
        signal_soxs = True
    if soxl_sma > soxs_sma or soxl_sma > soxl_close:
        signal_soxl = True

    # Determine the trade type for SOXS
    if signal_soxs and soxs_sma < soxs_close and account.get_shares("SOXS") > 0:
        trades.append(["Sell", "SOXS", no_soxs_shares])
    elif signal_soxs and soxs_sma > soxs_close and soxs_buy > 0:
        trades.append(["Buy", "SOXS", soxs_buy])

    # Determine the trade type for SOXL
    if signal_soxl and soxl_sma < soxl_close and account.get_shares("SOXL") > 0:
        trades.append(["Sell", "SOXL", no_soxl_shares])
    elif signal_soxl and soxl_sma > soxl_close and soxl_buy > 0:
        trades.append(["Buy", "SOXL", soxl_buy])

    # Print the trades
    for trade in trades:
        print(f"Trade - Type: {trade[0]}, Symbol: {trade[1]}, Volume: {trade[2]}")

    return trades

def execute_trades(trade, account):  
    # Get the trade type, stock, the number of shares in trade, and price
    trade_type = trade[0]
    stock = trade[1]
    no_of_shares = trade[2]
    price = close_soxs_values[-1] if stock == "SOXS" else close_soxl_values[-1]

    # # Print the account information
    # print("\nAccount Information before trade:")
    # account.print_account()

    # Execute the trade
    if trade_type == "Buy":
        account.buy_stock(stock, no_of_shares, price)
    elif trade_type == "Sell":
        account.sell_stock(stock, no_of_shares, price)

    # # Print the account information
    # print("\nAccount Information after trade:")
    # account.print_account()

def load_data():
    try:
        with open('soxs_historical_data.json') as fs, open('soxl_historical_data.json') as fl:
            soxs_data = json.load(fs)
            soxl_data = json.load(fl)
        return soxs_data, soxl_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None




def start_trading_system(account, s_period, l_period):
    # Open JSON files
    fs, fl = open_JSON_files()

    # Read JSON files
    soxs_data, soxl_data = load_data()

    # Initialize the CSV file
    initialize_csv_file()

    # Simulate time loop from beginning of historical data
    for soxs,soxl in zip(soxs_data.items(), soxl_data.items()):
        # Print the date
        print("\nDate: " + get_date(soxs))

        # Calculate and print simple moving averages for both stocks
        soxs_sma = calc_sma("SOXS", soxs, s_period)
        soxl_sma = calc_sma("SOXL", soxl, l_period)

        # Skip evaluation of sma values if not enough data
        if soxs_sma is None or soxl_sma is None:
            continue

        # Print account summary
        account.print_account()

        # Determine buy/sell signals
        trades = EvaluateSMA(soxs_sma, soxl_sma, account)

        # Skip if no trades
        if len(trades) == 0:
            continue;

        # Execute trades
        for trade in trades:
            execute_trades(trade, account)
            write_trade_to_csv(trade, account, soxs, soxl)

    # Write final summary to CSV
    write_final_summary_to_csv(account)

    # Close JSON files
    close_JSON_files(fs, fl)

def main():
    # Download historical data
    download_data()

    # Create account for investor, using default 100,000 starting balance
    account = Account()

    # Set the short and long periods
    s_period = 50
    l_period = 200

    # Ask for user input
    # ui.get_user_input()

    # Start the trading system
    start_trading_system(account, s_period, l_period)

    
if __name__ == "__main__":
    date_range = None  # Initialize date_range variable
    
    while True:
        print("1. Download Data")
        print("2. Input Date Range" )
        print("3. Run Trading System")
        print("4. Draw Graph Based on Date Range")
        print("5. Print Account Information")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        # Option 1 to download data
        if choice == "1":
            download_data()
        
        # Option 2 ask user input for date range
        elif choice == "2":
            start_date, end_date = get_date_range_from_user()
            if start_date and end_date:
                date_range = (start_date, end_date)
                print(f"Date range set from {start_date} to {end_date}.")
        
        # Option 3 run trading system
        elif choice == "3":
            main()
        
        # Option 4 draw graph
        elif choice == "4":
            if date_range:
                plot_graph(date_range)
            else: # Make user input date range before drawing graph
                print("Please set a date range first (Option 3).")
        
        # Option 5 print account information
        # Might remove this one later
        elif choice == "5":
            if 'date_range' in locals():
                main()  # Call main function to print account information
            else:
                print("Please set a date range first (Option 3).")
        # Exit menu and terminate execution
        elif choice == "6":
            break
        
        else:
            print("Invalid choice. Please try again.")