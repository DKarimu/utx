# /app/apps/data/models/ticker.py
from datetime import datetime

from django.db import connection, models


class Ticker(models.Model):
    id = models.BigAutoField(primary_key=True)
    last = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Ticker - {self.timestamp}"

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
        return cls.objects.get(id=ticker_data_id)

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

    class Meta:
        app_label = "data"  # Explicitly set the app_label to 'data'
