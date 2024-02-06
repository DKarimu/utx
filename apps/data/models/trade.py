# /app/apps/data/models/trade.py
import logging
from datetime import datetime

from django.db import models

logger = logging.getLogger(__name__)


class Trade(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    id = models.FloatField()
    rate = models.CharField(max_length=20)
    amount = models.CharField(max_length=20)
    order_type = models.CharField(max_length=10)
    time_in_force = models.CharField(max_length=20)
    stop_loss_rate = models.DateTimeField()
    pair = models.DateTimeField()
    utx_create_time = models.DateTimeField()

    def __str__(self):
        ticker_dict = {
            "utx_trade ID": self.utx_id,
            "last": self.id,
            "bid": self.amount,
            "ask": self.rate,
            "high": self.pair,
            "low": self.order_type,
            "volume": self.created_at,
            "timestamp": self.utx_create_time,
        }
        return str(ticker_dict)

    @classmethod
    def create_trade_data(cls, data):
        return cls.objects.create(
            id=data["id"],
            amount=data["amount"],
            rate=data["rate"],
            pair=data["pair"],
            order_type=data["order_type"],
            created_at=data["created_at"],
        )

    @classmethod
    def read_all_trade_data(cls):
        return cls.objects.all()

    @classmethod
    def read_trade_data_by_id(cls, trade_data_id):
        return cls.objects.get(utx_id=trade_data_id)

    def update_trade_data(self, data):
        self.id = data["id"]
        self.amount = data["amount"]
        self.rate = data["rate"]
        self.pair = data["pair"]
        self.order_type = data["order_type"]
        self.created_at = data["created_at"]
        self.save()

    def delete_trade_data(self):
        self.delete()

    def create_trades_data(public_trades):
        trades_data = public_trades.get("data", [])
        for trade_data in trades_data:
            Trade.create_trade_data(trade_data)

    def save(self, *args, **kwargs):
        try:
            if not self.utx_create_time:
                current_time = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
                self.utx_create_time = datetime.strptime(
                    current_time, "%Y%m%d%H%M%S.%f"
                )
            super(Trade, self).save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving {self.__class__.__name__} instance: {e}")
            raise

    def delete(self, *args, **kwargs):
        try:
            super(Trade, self).delete(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting {self.__class__.__name__} instance: {e}")
            raise

    class Meta:
        app_label = "data"  # Explicitly set the app_label to 'data'
