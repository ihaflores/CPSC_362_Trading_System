import database as db
import trading_system as ts

def main():
    # Create database object
    database = db.DataBase()

    # Create data access interface object
    data_access = db.DataAccessAdapter(database)

    # Download data
    data_access.download_data()

    # Create account for investor, using default 100,000 starting balance
    account = ts.Account()

    # Create account interface object
    account_interface = ts.AccountInterface(account)

    # Set the short and long periods
    s_period = 50
    l_period = 200

    # Ask for user input
    # ui.get_user_input()

    # Start the trading system
    ts.start_trading_system(account_interface, s_period, l_period, data_access)

    
if __name__ == "__main__":
    main()