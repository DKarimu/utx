from datetime import datetime

from django.test import TestCase
from models.ticker import Ticker


class TickerModelTest(TestCase):

    def setUp(self):
        Ticker.objects.create(
            last=100.0,
            bid=99.0,
            ask=101.0,
            high=102.0,
            low=98.0,
            volume=1500.0,
            timestamp=datetime.now(),
        )

    def test_ticker_creation(self):
        ticker = Ticker.objects.get(last=100.0)
        self.assertEqual(ticker.bid, 99.0)
        self.assertEqual(ticker.ask, 101.0)

    def test_update_ticker_data(self):
        ticker = Ticker.objects.get(last=100.0)
        update_data = {
            "last": 105.0,
            "bid": 104.0,
            "ask": 106.0,
            "high": 107.0,
            "low": 103.0,
            "volume": 2000.0,
            "timestamp": datetime.timestamp(datetime.now()),
        }
        ticker.update_ticker_data(update_data)
        ticker.refresh_from_db()

        self.assertEqual(ticker.last, 105.0)
        self.assertEqual(ticker.volume, 2000.0)
