import datetime
import matplotlib.pyplot as plt

def display_graph(symbol, start_date, end_date):
    from trading_system import load_data  # Import load_data() inside the function

    soxs_data, soxl_data = load_data()
    if symbol == "SOXS":
        data = soxs_data
    else:
        data = soxl_data

    dates = []
    closes = []

    for date, values in data.items():
            if start_date <= date <= end_date:
                dates.append(datetime.datetime.fromisoformat(date))  # Convert to datetime object
                closes.append(values["Close"])

    tick_frequency = max(1, len(dates) // 10)  # Show only 10 labels max
    plt.xticks(dates[::tick_frequency], rotation=45)
    plt.figure(figsize=(15, 10))
    plt.plot(dates, closes, label=f'{symbol} Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'Historical Close Price of {symbol}')
    plt.legend()
    plt.show()

def get_user_input():
    symbol = input("Enter the symbol (SOXS or SOXL): ").upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    display_graph(symbol, start_date, end_date)