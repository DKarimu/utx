# test_coincheck_client.py

from django.test import SimpleTestCase

from brokers.coincheck_client import CoincheckClient


class TestCoincheckClient(SimpleTestCase):
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
        self.assertTrue("error", res)

        res = coincheck.get_transaction_history_pagination()
        self.assertTrue("error", res)

        res = coincheck.get_balance()
        self.assertTrue("error", res)

        purpose_details = {
            "specific_items_of_goods": "食料品",
            "place_of_origin": "カナダ",
            "place_of_loading": "アメリカ",
        }
        res = coincheck.get_send_crypto_currency(
            1069725, "0.000001", "payment_of_importing", purpose_details
        )
        self.assertTrue("error", res)

        res = coincheck.get_send_crypto_history("btc_jpy")
        self.assertTrue("error", res)

        res = coincheck.get_deposits_istory("btc_jpy")
        self.assertTrue("error", res)

        res = coincheck.get_account_information()
        self.assertTrue("error", res)

        res = coincheck.get_bank_account_list()
        self.assertTrue("error", res)

        res = coincheck.get_withdraw_history()
        self.assertTrue("error", res)

        res = coincheck.post_create_withdraw(1069725, "10000.0", "JPY")
        self.assertTrue("error", res)
