# test_coincheck_client.py
# run test CMD
# python manage.py test brokers.test.test_coincheck_client

from django.test import SimpleTestCase
from brokers.coincheck_client import CoincheckClient


class TestCoincheckClient(SimpleTestCase):
    def test_ticker_returns_error(self):
        coincheck_client = CoincheckClient()

        # Test For Coincheck Public API
        result = coincheck_client.get_ticker("etc_jpy")
        self.assertNotIn("error", result)

        result = coincheck_client.get_trades()
        self.assertNotIn("error", result)

        result = coincheck_client.get_orderbooks()
        self.assertNotIn("error", result)

        result = coincheck_client.get_calc_rate("btc_jpy", "buy", "1", "28000")
        self.assertNotIn("error", result)

        result = coincheck_client.get_standard_rate("btc_jpy")
        self.assertNotIn("error", result)

        # Test For Coincheck Private API
        result = coincheck_client.post_new_order("btc_jpy", "buy", "6328998.0", "10")
        self.assertTrue("error", result)

        result = coincheck_client.get_unsettled_order_list()
        self.assertNotIn("error", result)
