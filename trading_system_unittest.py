import unittest
import os
import trading_system as ts
from trading_system import Account

class TestAccount(unittest.TestCase):
    def test_init(self):
        account = Account()
        self.assertEqual(account.balance, 100000)
    def test_init_with_balance(self):
        account = Account(50000)
        self.assertEqual(account.balance, 50000)
    def test_buy(self):
        account = Account()
        account.buy_stock("SOXS", 100, 10)
        self.assertEqual(account.balance, 99000)
    def test_sell(self):
        account = Account()
        account.buy_stock("SOXL", 100, 10)
        account.sell_stock("SOXL", 50, 10)
        self.assertEqual(account.balance, 99500)

class TestTradingSystem(unittest.TestCase):
    def test_initiazlize_csv_file(self):
        ts.initialize_csv_file()
        self.assertTrue(os.path.exists("trades.csv"))

    def test_calc_sma(self):
        # Create all data needed for calc_sma()
        s_period = 5
        l_period = 10

        # Create dummy data
        soxs_data = [0,{'Close': 10}]
        soxl_data = [0,{'Close': 19}]
        ts.close_soxs_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ts.close_soxl_values = [11, 12, 13, 15, 17, 19, 18, 18, 20]

        # Calculate the SMA 
        soxs_sma = ts.calc_sma('SOXS', soxs_data, s_period)
        soxl_sma = ts.calc_sma('SOXL', soxl_data, l_period)

        # Check the SMA values
        self.assertEqual(soxs_sma, (6+7+8+9+10)/5)
        self.assertEqual(soxl_sma, (11+12+13+15+17+19+18+18+20+19)/10)

    def test_calc_gain_loss(self):
        # Create data for calc_gain_loss()
        price = 10
        purchase_price = 5
        self.assertEqual(ts.calc_gain_loss(price, purchase_price), 100.00)

        price = 5
        purchase_price = 10
        self.assertEqual(ts.calc_gain_loss(price, purchase_price), -50.00)

        price = 5
        purchase_price = 5
        self.assertEqual(ts.calc_gain_loss(price, purchase_price), 0.00)

    def test_EvaluateSMA(self):
        # Buy SOXL test
        account = Account()
        soxs_sma = 10
        soxl_sma = 20
        ts.close_soxs_values = [9]
        ts.close_soxl_values = [19]
        trades = ts.EvaluateSMA(soxs_sma, soxl_sma, account)
        expected_trades = [["Buy", "SOXL", (account.get_balance()*0.05 // ts.close_soxl_values[-1])]]
        self.assertTrue(expected_trades == trades)

        # Buy SOXS test
        account = Account()
        soxs_sma = 20
        soxl_sma = 10
        ts.close_soxs_values = [19]
        ts.close_soxl_values = [11]
        trades = ts.EvaluateSMA(soxs_sma, soxl_sma, account)
        expected_trades = [["Buy", "SOXS", (account.get_balance()*0.1 // ts.close_soxs_values[-1])]]
        self.assertTrue(expected_trades == trades)

        # Sell SOXS test
        account = Account()
        account.buy_stock("SOXS", 100, 10)
        soxs_sma = 20
        soxl_sma = 5
        ts.close_soxs_values = [21]
        ts.close_soxl_values = [5]
        trades = ts.EvaluateSMA(soxs_sma, soxl_sma, account)
        expected_trades = [["Sell", "SOXS", account.get_shares("SOXS")]]
        self.assertTrue(expected_trades == trades)

        # Sell SOXL test
        account = Account()
        account.buy_stock("SOXL", 100, 10)
        soxs_sma = 5
        soxl_sma = 20
        ts.close_soxs_values = [5]
        ts.close_soxl_values = [21]
        trades = ts.EvaluateSMA(soxs_sma, soxl_sma, account)
        expected_trades = [["Sell", "SOXL", account.get_shares("SOXL")]]
        self.assertTrue(expected_trades == trades)

    def test_execute_trades(self):
        ts.close_soxl_values = [10]
        ts.close_soxs_values = [20]

        account = Account()
        trade = ["Buy", "SOXL", 10]
        ts.execute_trades(trade, account)
        self.assertEqual(account.get_shares("SOXL"), 10)
        self.assertEqual(account.get_balance(), 99900)
        
        account = Account()
        account.buy_stock("SOXS", 100, 15)
        trade = ["Sell", "SOXS", 50]
        ts.close_soxs_values.append(30)
        ts.execute_trades(trade, account)
        self.assertEqual(account.get_shares("SOXS"), 50)
        self.assertEqual(account.get_balance(), 100000-1500 + 50*30)

if __name__ == '__main__':
    unittest.main()