from datetime import datetime

from django.db import models


class MarketData(models.Model):
    id = models.BigAutoField(primary_key=True)
    last = models.FloatField()
    bid = models.FloatField()
    ask = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"MarketData - {self.timestamp}"

    @classmethod
    def create_market_data(cls, data):
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
    def read_all_market_data(cls):
        return cls.objects.all()

    @classmethod
    def read_market_data_by_id(cls, market_data_id):
        return cls.objects.get(id=market_data_id)

    def update_market_data(self, data):
        self.last = data["last"]
        self.bid = data["bid"]
        self.ask = data["ask"]
        self.high = data["high"]
        self.low = data["low"]
        self.volume = data["volume"]
        self.timestamp = datetime.fromtimestamp(data["timestamp"])
        self.save()

    def delete_market_data(self):
        self.delete()
