import logging

from django.db import models
from util import UtxUtils

logger = logging.getLogger(__name__)


class Trade(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    id = models.FloatField()
    amount = models.CharField(max_length=20)
    rate = models.CharField(max_length=20)
    pair = models.CharField(max_length=10)
    order_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_trade_data(cls, data):
        return cls.objects.create(**data)

    @staticmethod
    def create_trades_data(public_trades):
        trades_data = public_trades.get("data", [])
        for trade_data in trades_data:
            Trade.create_trade_data(trade_data)

    def save(self, *args, **kwargs):
        try:
            self.utx_id = UtxUtils().generate_utx_id()
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Trade instance: {e}")
            pass

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting Trade instance: {e}")
            pass

    class Meta:
        app_label = "data"
