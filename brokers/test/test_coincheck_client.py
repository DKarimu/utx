# test_coincheck_client.py
# run test CMD
# python manage.py test brokers.test.test_coincheck_client

from django.test import SimpleTestCase
from brokers.coincheck_client import CoincheckClient


class TestCoincheckClient(SimpleTestCase):
    def test_ticker_returns_error(self):
        coincheck_client = CoincheckClient()

        result = coincheck_client.ticker()
        self.assertNotIn("error", result)

        result = coincheck_client.trades("btc_jpy")
        self.assertNotIn("error", result)

        result = coincheck_client.orderbooks()
        self.assertNotIn("error", result)
