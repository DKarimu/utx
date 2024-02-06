# /app/apps/data/models/order.py
import logging
from datetime import datetime

from django.db import models

logger = logging.getLogger(__name__)
from django.db import models


class Order(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    success = models.BooleanField()
    order_id = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=50)
    time_in_force = models.CharField(max_length=50)
    stop_loss_rate = models.DecimalField(max_digits=10, decimal_places=2)
    pair = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    utx_create_time = models.DateTimeField()

    def __str__(self):
        order_dict = {
            "utx_order ID": self.utx_id,
            "success": self.success,
            "order_id": self.order_id,
            "rate": self.rate,
            "amount": self.amount,
            "order_type": self.order_type,
            "time_in_force": self.time_in_force,
            "stop_loss_rate": self.stop_loss_rate,
            "pair": self.pair,
            "created_at": self.created_at,
            "utx_create_time": self.utx_create_time,
        }
        return str(order_dict)

    @classmethod
    def create_order_data(cls, data):
        return cls.objects.create(
            success=data["success"],
            order_id=data["order_id"],
            rate=data["rate"],
            amount=data["amount"],
            order_type=data["order_type"],
            time_in_force=data["time_in_force"],
            stop_loss_rate=data["stop_loss_rate"],
            pair=data["pair"],
            created_at=data["created_at"],
        )

    @classmethod
    def read_all_order_data(cls):
        return cls.objects.all()

    @classmethod
    def read_order_data_by_id(cls, order_data_id):
        return cls.objects.get(utx_id=order_data_id)

    def update_order_data(self, data):
        self.success = data["success"]
        self.order_id = data["order_id"]
        self.rate = data["rate"]
        self.amount = data["amount"]
        self.order_type = data["order_type"]
        self.time_in_force = data["time_in_force"]
        self.stop_loss_rate = data["stop_loss_rate"]
        self.pair = data["pair"]
        self.created_at = data["created_at"]
        self.save()

    def delete_order_data(self):
        self.delete()

    def save(self, *args, **kwargs):
        try:
            if not self.utx_create_time:
                current_time = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
                self.utx_create_time = datetime.strptime(
                    current_time, "%Y%m%d%H%M%S.%f"
                )
            super(Order, self).save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving {self.__class__.__name__} instance: {e}")
            raise

    def delete(self, *args, **kwargs):
        try:
            super(Order, self).delete(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting {self.__class__.__name__} instance: {e}")
            raise

    class Meta:
        app_label = "data"  # Explicitly set the app_label to 'data'
