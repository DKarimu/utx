from django.test import TestCase
from models.order_book import OrderBook


class OrderBookModelTests(TestCase):

    def test_order_book_creation(self):
        """Test the creation of an OrderBook instance."""
        order_book = OrderBook.objects.create(
            ask_price=100.00,
            ask_quantity=10.00,
            bid_price=95.00,
            bid_quantity=15.00,
        )
        self.assertTrue(isinstance(order_book, OrderBook))
        self.assertEqual(order_book.ask_price, 100.00)
        self.assertEqual(order_book.ask_quantity, 10.00)
        self.assertEqual(order_book.bid_price, 95.00)
        self.assertEqual(order_book.bid_quantity, 15.00)
