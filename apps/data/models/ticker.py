import logging
from datetime import datetime

from django.db import models
from util import UtxUtils

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

    @classmethod
    def create_ticker_data(cls, data):
        data.pop("id", None)
        if "timestamp" in data:
            data["timestamp"] = datetime.fromtimestamp(data["timestamp"])
        logger.debug(f"Creating Ticker with data: {data}")
        return cls.objects.create(
            utx_id=data.get("utx_id"),
            last=data.get("last"),
            bid=data.get("bid"),
            ask=data.get("ask"),
            high=data.get("high"),
            low=data.get("low"),
            volume=data.get("volume"),
            timestamp=data.get("timestamp"),  # Already converted to datetime if present
        )

    @classmethod
    def read_all_ticker_data(cls):
        return cls.objects.all()

    @classmethod
    def read_ticker_data_by_id(cls, ticker_data_id):
        return cls.objects.get(utx_id=ticker_data_id)

    def update_ticker_data(self, data):
        for field, value in data.items():
            if field == "timestamp":
                value = datetime.fromtimestamp(value)
            setattr(self, field, value)
        self.save()

    def save(self, *args, **kwargs):
        try:
            self.utx_id = UtxUtils().generate_utx_id()
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Trade instance: {e}")
            pass

    class Meta:
        app_label = "data"
        ordering = ["-timestamp"]
