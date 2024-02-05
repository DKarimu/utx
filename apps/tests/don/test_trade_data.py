from django.test import TestCase
from models.trade import Trade


class TestTrade(TestCase):
    def test_trade_data_operations(self):
        # Create
        data_to_create = {
            "id": 81,
            "amount": "0.1",
            "rate": "36120.0",
            "pair": "btc_jpy",
            "order_type": "buy",
            "created_at": "2015-01-09T15:25:13.000Z",
        }

        trade_data_created = Trade.create_trade_data(data_to_create)
        self.assertIsNotNone(trade_data_created.utx_id)

        # Read all
        all_trade_data = Trade.read_all_trade_data()
        self.assertTrue(all_trade_data.exists())

        # Read by ID
        trade_data_by_id = Trade.read_trade_data_by_id(trade_data_created.utx_id)
        self.assertEqual(trade_data_by_id, trade_data_created)

        # Update
        updated_data = {
            "id": 81,
            "amount": "0.1",
            "rate": "36120.0",
            "pair": "btc_jpy",
            "order_type": "sell",
            "created_at": "2015-01-09T15:25:13.000Z",
        }

        trade_data_created.update_trade_data(updated_data)
        trade_data_after_update = Trade.read_trade_data_by_id(trade_data_created.utx_id)

        self.assertEqual(trade_data_after_update.id, updated_data["id"])
        self.assertEqual(trade_data_after_update.order_type, updated_data["order_type"])
        # Continue with other fields...

        # Delete
        trade_data_created.delete_trade_data()
        self.assertFalse(Trade.read_all_trade_data().exists())
