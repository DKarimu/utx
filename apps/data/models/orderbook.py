# /app/apps/data/models/order_book.py
from datetime import datetime

from django.db import models


class OrderBook(models.Model):
    utx_id = models.BigAutoField(primary_key=True)
    ask_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ask_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bid_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    utx_create_time = models.DateTimeField()

    @classmethod
    def create_order_book(cls, data):
        ask_data = data["asks"]
        bid_data = data["bids"]

        # Create ask and bid entries
        ask_entries = []
        bid_entries = []

        for (ask_price, ask_quantity), (bid_price, bid_quantity) in zip(
            ask_data, bid_data
        ):
            entry = cls.objects.create(
                ask_price=ask_price,
                ask_quantity=ask_quantity,
                bid_price=bid_price,
                bid_quantity=bid_quantity,
            )
            ask_entries.append([entry.ask_price, str(entry.ask_quantity)])
            bid_entries.append([entry.bid_price, str(entry.bid_quantity)])

        return {"asks": ask_entries, "bids": bid_entries}

    @classmethod
    def get_order_book(cls):
        order_book = {
            "asks": [],
            "bids": [],
        }

        # Fetch all entries and populate order_book
        for entry in cls.objects.all():
            if entry.ask_price is not None:
                order_book["asks"].append([entry.ask_price, str(entry.ask_quantity)])
            elif entry.bid_price is not None:
                order_book["bids"].append([entry.bid_price, str(entry.bid_quantity)])

        return order_book

    @classmethod
    def delete_order_book(cls):
        cls.objects.all().delete()

    def save(self, *args, **kwargs):
        # Check if utx_create_time is not set
        if not self.utx_create_time:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:-3]
            self.utx_create_time = datetime.strptime(current_time, "%Y%m%d%H%M%S.%f")
        super(OrderBook, self).save(*args, **kwargs)

    class Meta:
        app_label = "data"  # Explicitly set the app_label to 'data'
