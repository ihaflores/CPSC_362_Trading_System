import csv
import os
from model import Account, download_data, load_data, calc_sma, calc_gain_loss
from view import View, get_user_input

close_soxs_values = []  # Initialize as an empty list
close_soxl_values = []  # Initialize as an empty list

class Controller:
    def __init__(self):
        self.model = Account()
        self.view = View()

    def download_data(self):
        download_data()

    def start_trading_system(self, s_period, l_period):
        soxs_data, soxl_data = load_data()
        self.initialize_csv_file()
        for soxs, soxl in zip(soxs_data.items(), soxl_data.items()):
            date = soxs[0]
            soxs_sma = calc_sma("SOXS", soxs[1], s_period)
            soxl_sma = calc_sma("SOXL", soxl[1], l_period)
            if soxs_sma is None or soxl_sma is None:
                continue
            self.view.print_account(self.model)
            trades = self.evaluate_sma(soxs_sma, soxl_sma)
            for trade in trades:
                self.execute_trades(trade)
                self.write_trade_to_csv(trade, date, soxs, soxl)
        self.write_final_summary_to_csv()

    def display_graph(self, symbol, start_date, end_date):
        soxs_data, soxl_data = load_data()
        data = soxs_data if symbol == "SOXS" else soxl_data
        self.view.display_graph(symbol, data, start_date, end_date)

    def execute_trades(self, trade):
        trade_type = trade[0]
        stock = trade[1]
        no_of_shares = trade[2]
        price = close_soxs_values[-1] if stock == "SOXS" else close_soxl_values[-1]
        if trade_type == "Buy":
            self.model.buy_stock(stock, no_of_shares, price)
        elif trade_type == "Sell":
            self.model.sell_stock(stock, no_of_shares, price)

    def evaluate_sma(self, soxs_sma, soxl_sma):
        balance = self.model.get_balance()
        no_soxs_shares = self.model.get_shares("SOXS")
        no_soxl_shares = self.model.get_shares("SOXL")
        soxs_close = close_soxs_values[-1]
        soxl_close = close_soxl_values[-1]
        trades = []
        signal_soxs = soxs_sma > soxl_sma
        signal_soxl = soxl_sma > soxs_sma or soxl_sma > soxl_close
        soxs_buy = (balance * 0.1) // soxs_close
        soxl_buy = (balance * 0.05) // soxl_close
        if signal_soxs and soxs_sma < soxs_close and self.model.get_shares("SOXS") > 0:
            trades.append(["Sell", "SOXS", no_soxs_shares])
        elif signal_soxs and soxs_sma > soxs_close and soxs_buy > 0:
            trades.append(["Buy", "SOXS", soxs_buy])
        if signal_soxl and soxl_sma < soxl_close and self.model.get_shares("SOXL") > 0:
            trades.append(["Sell", "SOXL", no_soxl_shares])
        elif signal_soxl and soxl_sma > soxl_close and soxl_buy > 0:
            trades.append(["Buy", "SOXL", soxl_buy])
        return trades

    def initialize_csv_file(self):
        if os.path.exists("trades.csv"):
            os.remove("trades.csv")
        self.write_data_to_csv(['Date', 'Stock', 'Trade', 'No. of Shares', 'Price', 'Gain/Loss', '% Return', 'Balance'])

    def write_data_to_csv(self, data):
        with open('trades.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def write_trade_to_csv(self, trade, date, soxs, soxl):
        symbol = trade[1]
        buy_sell = trade[0]
        no_of_shares = int(trade[2])
        close_value = close_soxs_values[-1] if symbol == "SOXS" else close_soxl_values[-1]
        todays_return = self.model.calc_account_return()
        gain_loss = calc_gain_loss(close_value, (self.model.get_running_stock_balance(symbol) / no_of_shares)) if buy_sell == "Sell" else 0
        self.write_data_to_csv([date, symbol, buy_sell, no_of_shares, round(close_value, 2), gain_loss, todays_return, self.model.get_balance()])

    def write_final_summary_to_csv(self):
        self.write_data_to_csv(["Portfolio Lifetime Summary:"])
        self.write_data_to_csv(["Total Gain/Loss", "Total % Return", "Final Balance", "Final Portfolio Value"])
        total_gain_loss = round(self.model.get_portfolio_value() - self.model.get_initial_balance(), 2)
        total_account_return = self.model.calc_account_return()
        self.write_data_to_csv([total_gain_loss, total_account_return, self.model.get_balance(), round(self.model.get_portfolio_value(), 2)])

def main():
    controller = Controller()
    while True:
        print("1. Download Data")
        print("2. Run Trading System")
        print("3. Input Date & Draw Graph")
        print("4. Print Account Information")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            controller.download_data()
        elif choice == "2":
            controller.start_trading_system(50, 200)
        elif choice == "3":
            symbol, start_date, end_date = get_user_input()
            controller.display_graph(symbol, start_date, end_date)
        elif choice == "4":
            controller.view.print_account(controller.model)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()