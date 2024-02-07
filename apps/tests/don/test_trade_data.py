from django.test import TestCase
from models.trade import Trade


class TradeModelTest(TestCase):

    def setUp(self):
        self.trade_data = {
            "trade_id": 123.456,
            "amount": "1000",
            "rate": "0.01",
            "pair": "USD/EUR",
            "order_type": "buy",
        }
        self.trade = Trade.objects.create(**self.trade_data)

    def test_trade_creation(self):
        self.assertTrue(isinstance(self.trade, Trade))
        self.assertEqual(self.trade.trade_id, self.trade_data["trade_id"])

    def test_trade_str(self):
        expected_str = f"Trade {self.trade.utx_id}"
        self.assertEqual(str(self.trade), expected_str)

    def test_create_trade_data_class_method(self):
        new_trade_data = self.trade_data.copy()
        new_trade_data["trade_id"] = 654.321
        new_trade = Trade.create_trade_data(new_trade_data)
        self.assertTrue(isinstance(new_trade, Trade))
        self.assertEqual(new_trade.trade_id, new_trade_data["trade_id"])
