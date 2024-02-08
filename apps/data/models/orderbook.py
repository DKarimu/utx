import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class OrderBook(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    ask_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    ask_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    bid_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    bid_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    utx_create_time = models.DateTimeField(default=timezone.now)

    @classmethod
    def create_order_book(cls, data):
        ask_data = data.get("asks", [])
        bid_data = data.get("bids", [])
        entries = []

        for ask, bid in zip(ask_data, bid_data):
            entry = cls.objects.create(
                ask_price=ask[0],
                ask_quantity=ask[1],
                bid_price=bid[0],
                bid_quantity=bid[1],
            )
            entries.append(entry)

        return {
            "asks": [
                (entry.ask_price, entry.ask_quantity)
                for entry in entries
                if entry.ask_price
            ],
            "bids": [
                (entry.bid_price, entry.bid_quantity)
                for entry in entries
                if entry.bid_price
            ],
        }

    @classmethod
    def get_order_book(cls):
        entries = cls.objects.all()
        return {
            "asks": [
                (entry.ask_price, entry.ask_quantity)
                for entry in entries
                if entry.ask_price
            ],
            "bids": [
                (entry.bid_price, entry.bid_quantity)
                for entry in entries
                if entry.bid_price
            ],
        }

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving Order instance: {e}")
            pass

    def delete(self, *args, **kwargs):
        try:
            super().delete(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error deleting Order instance: {e}")
            pass

    @classmethod
    def delete_order_book(cls):
        cls.objects.all().delete()

    class Meta:
        app_label = "data"
