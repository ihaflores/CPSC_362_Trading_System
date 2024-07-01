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
            stock_display = StockDisplay()  # Create an observer

            stock.register(stock_display)  # Register observer to subject

            # Simulate updating the price and notifying observers with random prices
            for _ in range(50):  # You can adjust the number of iterations as needed
                # Generate a random price (example using random.randint())
                random_price = random.randint(1, 100)  # Example: Generates a random integer between 1 and 100
                stock.ask_price = random_price
                time.sleep(0.1)  # Adjust the delay time as needed (e.g., 0.1 seconds)

            stock.unregister(stock_display)  # Unregister observer from subject
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")