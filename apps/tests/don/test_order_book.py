# /app/apps/tests/test_order_book.py
from datetime import datetime

from django.test import TestCase
from django.utils import timezone
from models.orderbook import OrderBook


class OrderBookTest(TestCase):
    def setUp(self):
        # Set up initial data for testing
        self.order_book_data = {
            "asks": [
                [27330, "2.25"],
                [27340, "0.45"],
            ],
            "bids": [
                [27240, "1.1543"],
                [26800, "1.2226"],
            ],
        }

    def test_create_order_book(self):
        # Test the create_order_book method
        OrderBook.create_order_book(self.order_book_data)

        # Check if entries are created
        self.assertEqual(OrderBook.objects.count(), 2)

    def test_get_order_book(self):
        # Test the get_order_book method
        OrderBook.create_order_book(self.order_book_data)

        order_book = OrderBook.get_order_book()

        # Check if the order_book has the expected structure
        self.assertDictEqual(order_book, order_book)

        # Check if entries are updated
        updated_order_book = OrderBook.get_order_book()
        self.assertEqual(updated_order_book, updated_order_book)

    def test_delete_order_book(self):
        # Test the delete_order_book method
        OrderBook.create_order_book(self.order_book_data)

        OrderBook.delete_order_book()

        # Check if all entries are deleted
        self.assertEqual(OrderBook.objects.count(), 0)

    def test_save_method(self):
        # Test the save method
        order_book_entry = OrderBook(
            ask_price=27000,
            ask_quantity="1.75",
            bid_price=None,
            bid_quantity=None,
        )

        order_book_entry.save()

        # Check if utx_create_time is set
        self.assertIsNotNone(order_book_entry.utx_create_time)
