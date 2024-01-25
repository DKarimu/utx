# test_coincheck_client.py
# run test CMD
# python manage.py test brokers.test.test_coincheck_client
from django.test import TestCase
from unittest.mock import patch
from brokers.coincheck_client import CoincheckClient


class TestCoincheckClient(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up any test-specific configurations, mock data, etc.

    def setUp(self):
        self.coincheck_client = CoincheckClient()

    def test_ticker(self):
        with patch("brokers.coincheck_client.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"example": "ticker_data"}
            result = self.coincheck_client.ticker()

        # Assertions
        mock_get.assert_called_once_with(
            self.coincheck_client.construct_request_url("ticker")
        )
        self.assertEqual(result, {"example": "ticker_data"})

    def test_trades(self):
        # Similar structure as the test_ticker method
        pass

    def test_orderbooks(self):
        # Similar structure as the test_ticker method
        pass

    # Add more test methods for other functionalities as needed

    def tearDown(self):
        # Clean up any resources if necessary
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Clean up any class-level resources if necessary
