# test_coincheck_client.py
# run test CMD
# python manage.py test brokers.test.test_coincheck_client

import logging
from django.test import SimpleTestCase
from utx_logger import UtxLogger as log
from brokers.coincheck_client import CoincheckClient


class TestCoincheckClient(SimpleTestCase):
    def __int__(self):
        self.log = log(self.__class__.__name__)

    def test_ticker_returns_error(self):
        coincheck = CoincheckClient()

        # Test For Coincheck Public API
        res = coincheck.get_ticker("etc_jpy")
        self.assertNotIn("error", res)

        res = coincheck.get_trades()
        self.assertNotIn("error", res)

        res = coincheck.get_orderbooks()
        self.assertNotIn("error", res)

        res = coincheck.get_calc_rate("btc_jpy", "buy", "1", "28000")
        self.assertNotIn("error", res)

        res = coincheck.get_standard_rate("btc_jpy")
        self.assertNotIn("error", res)

        # Test For Coincheck Private API
        res = coincheck.post_new_order("btc_jpy", "buy", "6328998.0", "10")
        self.assertTrue("error", res)

        res = coincheck.get_unsettled_order_list()
        self.assertNotIn("error", res)

        res = coincheck.delet_cancel_order("01")
        self.assertTrue("error", res)

        res = coincheck.get_order_cancellation_status("01")
        self.assertTrue("error", res)

        res = coincheck.get_transaction_history()
        # self.log.info("", res)
        self.assertTrue("error", res)
