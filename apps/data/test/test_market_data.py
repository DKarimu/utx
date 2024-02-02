from datetime import datetime

from django.test import TestCase

from apps.data.models.market_data import MarketData


class MarketDataTest(TestCase):
    def test_market_data_operations(self):
        # Create
        data_to_create = {
            "last": 100.0,
            "bid": 98.5,
            "ask": 101.2,
            "high": 105.0,
            "low": 97.8,
            "volume": 5000.0,
            "timestamp": datetime.now().timestamp(),
        }

        market_data_created = MarketData.create_market_data(data_to_create)
        self.assertIsNotNone(market_data_created.id)

        # Read all
        all_market_data = MarketData.read_all_market_data()
        self.assertTrue(all_market_data.exists())

        # Read by ID
        market_data_by_id = MarketData.read_market_data_by_id(market_data_created.id)
        self.assertEqual(market_data_by_id, market_data_created)

        # Update
        updated_data = {
            "last": 110.0,
            "bid": 108.5,
            "ask": 111.2,
            "high": 115.0,
            "low": 107.8,
            "volume": 6000.0,
            "timestamp": datetime.now().timestamp(),
        }

        market_data_created.update_market_data(updated_data)
        market_data_after_update = MarketData.read_market_data_by_id(
            market_data_created.id
        )

        self.assertEqual(market_data_after_update.last, updated_data["last"])
        self.assertEqual(market_data_after_update.bid, updated_data["bid"])
        # Continue with other fields...

        # Delete
        market_data_created.delete_market_data()
        self.assertFalse(MarketData.read_all_market_data().exists())
