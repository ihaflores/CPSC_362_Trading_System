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
    def test_download_data(self):
        ts.download_data()
        self.assertTrue(os.path.exists("soxs_historical_data.json"))
        self.assertTrue(os.path.exists("soxl_historical_data.json"))

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

if __name__ == '__main__':
    unittest.main()