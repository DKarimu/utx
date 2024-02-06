from datetime import datetime

from django.test import TestCase
from models.ticker import Ticker


class TickerTest(TestCase):
    def test_ticker_data_operations(self):
        # Create
        data_to_create = {
            "last": 100.0,
            "bid": 98.5,
            "ask": 101.2,
            "high": 105.0,
            "low": 97.8,
            "volume": 5000.0,
            "timestamp": 1644061482,
        }

        ticker_data_created = Ticker.create_ticker_data(data_to_create)
        self.assertIsNotNone(ticker_data_created.utx_id)

        # Read all
        all_ticker_data = Ticker.read_all_ticker_data()
        self.assertTrue(all_ticker_data.exists())

        # Read by ID
        ticker_data_by_id = Ticker.read_ticker_data_by_id(ticker_data_created.utx_id)
        self.assertEqual(ticker_data_by_id, ticker_data_created)

        # Update
        updated_data = {
            "last": 110.0,
            "bid": 108.5,
            "ask": 111.2,
            "high": 115.0,
            "low": 107.8,
            "volume": 6000.0,
            "timestamp": 1644061482,
        }

        ticker_data_created.update_ticker_data(updated_data)
        ticker_data_after_update = Ticker.read_ticker_data_by_id(
            ticker_data_created.utx_id
        )

        self.assertEqual(ticker_data_after_update.last, updated_data["last"])
        self.assertEqual(ticker_data_after_update.bid, updated_data["bid"])
        # Continue with other fields...

        # Delete
        ticker_data_created.delete_ticker_data()
        self.assertFalse(Ticker.read_all_ticker_data().exists())
