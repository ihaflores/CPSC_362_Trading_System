import unittest
from unittest.mock import patch
import ui
import trading_system as ts
import os

class TestTradingSystemIntegration(unittest.TestCase):

    def test_trading_system(self):
        # Initialize an account with a default balance
        account = ts.Account()

        # Set the short and long periods
        s_period = 50
        l_period = 200

        # Download historical data
        ts.download_data()

        # Start the trading system
        ts.start_trading_system(account, s_period, l_period)

        # Check if the trades.csv file is created
        self.assertTrue(os.path.exists("trades.csv"), "trades.csv file was not created")

        print("Integration test passed!")

    @patch('ui.display_graph')
    @patch('builtins.input', side_effect=['SOXS', '2023-01-01', '2023-12-31'])
    def test_display_graph_symbol(self, mock_input, mock_display_graph):
        # Call get_user_input which internally calls display_graph
        ui.get_user_input()
        
        # Check if display_graph was called with the correct symbol
        mock_display_graph.assert_called_once()
        called_args = mock_display_graph.call_args[0]
        symbol = called_args[0]
        
        self.assertIn(symbol, ["SOXS", "SOXL"], "Symbol is not valid. Must be 'SOXS' or 'SOXL'")

        print("Symbol validation test passed!")

if __name__ == "__main__":
    unittest.main()

