from datetime import datetime

from django.db import models
from django.utils.dateparse import parse_datetime


class Trade(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    id = models.DecimalField(max_digits=20, decimal_places=2)
    amount = models.CharField(max_length=20)
    rate = models.CharField(max_length=20)
    pair = models.CharField(max_length=20)
    order_type = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    utx_create_time = models.DateTimeField()

    def __str__(self):
        ticker_dict = {
            "Trade ID": self.utx_id,
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
        # Check if utx_create_time is not set
        if not self.utx_create_time:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
            self.utx_create_time = datetime.strptime(current_time, "%Y%m%d%H%M%S.%f")
        super(Trade, self).save(*args, **kwargs)

    class Meta:
        app_label = "data"  # Explicitly set the app_label to 'data'
