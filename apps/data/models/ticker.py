# /app/apps/data/models/ticker.py
import logging
from datetime import datetime

from django.db import models

logger = logging.getLogger(__name__)


class Ticker(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    last = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    timestamp = models.DateTimeField()
    utx_create_time = models.DateTimeField()

    def __str__(self):
        ticker_dict = {
            "utx_ticker ID": self.utx_id,
            "last": self.last,
            "bid": self.bid,
            "ask": self.ask,
            "high": self.high,
            "low": self.low,
            "volume": self.volume,
            "timestamp": self.timestamp,
        }
        return str(ticker_dict)

    @classmethod
    def create_ticker_data(cls, data):
        timestamp = datetime.fromtimestamp(data["timestamp"])
        return cls.objects.create(
            last=data["last"],
            bid=data["bid"],
            ask=data["ask"],
            high=data["high"],
            low=data["low"],
            volume=data["volume"],
            timestamp=timestamp,
        )

    @classmethod
    def read_all_ticker_data(cls):
        return cls.objects.all()

    @classmethod
    def read_ticker_data_by_id(cls, ticker_data_id):
        return cls.objects.get(utx_id=ticker_data_id)

    def update_ticker_data(self, data):
        self.last = data["last"]
        self.bid = data["bid"]
        self.ask = data["ask"]
        self.high = data["high"]
        self.low = data["low"]
        self.volume = data["volume"]
        self.timestamp = datetime.fromtimestamp(data["timestamp"])
        self.save()

    def delete_ticker_data(self):
        self.delete()

    def save(self, *args, **kwargs):
        try:
            if not self.utx_create_time:
                current_time = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
                self.utx_create_time = datetime.strptime(
                    current_time, "%Y%m%d%H%M%S.%f"
                )
            super(Ticker, self).save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving {self.__class__.__name__} instance: {e}")
            raise

    def delete(self, *args, **kwargs):
        try:
            super(Ticker, self).delete(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting {self.__class__.__name__} instance: {e}")
            raise

    class Meta:
        app_label = "data"  # Explicitly set the app_label to 'data'
