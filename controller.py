from model import Account, download_data, start_trading_system
import view

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
        print("4. Print Account Information")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            download_data()
        elif choice == "2":
            main()
        elif choice == "3":
            view.main()  # Call ui.py function to display the graph
        elif choice == "4":
            # Account info display logic here
            pass
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")