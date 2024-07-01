from model import Account, download_data, start_trading_system
import view
import time
import random
from view import Stock, StockDisplay

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
    while True:
        print("1. Download Data")
        print("2. Run Trading System")
        print("3. Input Date & Draw Graph")
        print("4. Display Current Stock Price")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            download_data()
        elif choice == "2":
            main()
        elif choice == "3":
            view.main()  # Call ui.py function to display the graph
        elif choice == "4":
            stock = Stock()  # Create a subject
            
            display = StockDisplay()  # Create an observer

            stock._obj_container.append(display)  # Subscribe observer to subject

            stock.simulate_price_change()  # Simulate price changes

            stock._obj_container.remove(display)  #
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")