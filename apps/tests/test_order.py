from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from models.order import Order


class OrderTest(TestCase):

    def setUp(self):
        self.order_data = {
            "success": True,
            "order_id": "ABC123",
            "rate": 12.34,
            "amount": 56.78,
            "order_type": "buy",
            "time_in_force": "GTC",
            "stop_loss_rate": 10.0,
            "pair": "BTC/USD",
            "created_at": timezone.now(),
        }

        self.order = Order.create_order_data(self.order_data)


def test_order_creation(self):
    self.assertTrue(isinstance(self.order, Order))

    expected_str = str(
        {
            "utx_order ID": self.order.utx_id,
            "success": self.order_data["success"],
            "order_id": self.order_data["order_id"],
            "rate": str(self.order_data["rate"]),
            "amount": str(self.order_data["amount"]),
            "order_type": self.order_data["order_type"],
            "time_in_force": self.order_data["time_in_force"],
            "stop_loss_rate": str(self.order_data["stop_loss_rate"]),
            "pair": self.order_data["pair"],
            "created_at": str(self.order_data["created_at"]),
            "utx_create_time": str(self.order_data["utx_create_time"]),
        }
    )

    self.assertEqual(str(self.order), expected_str)

    def test_read_all_order_data(self):
        orders = Order.read_all_order_data()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders[0], self.order)

    def test_read_order_data_by_id(self):
        retrieved_order = Order.read_order_data_by_id(self.order.utx_id)
        self.assertEqual(retrieved_order, self.order)

    def test_update_order_data(self):
        updated_data = {
            "success": False,
            "order_id": "XYZ789",
            "rate": 9.99,
            "amount": 123.45,
            "order_type": "sell",
            "time_in_force": "IOC",
            "stop_loss_rate": 15.0,
            "pair": "ETH/USD",
            "created_at": timezone.now(),
        }
        self.order.update_order_data(updated_data)
        updated_order = Order.read_order_data_by_id(self.order.utx_id)

        for key, value in updated_data.items():
            # Convert Decimal to float for comparison
            if isinstance(value, Decimal):
                value = float(value)
            self.assertEqual(updated_order[key], value)

    def test_delete_order_data(self):
        order_id = self.order.utx_id
        self.order.delete_order_data()
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(utx_id=order_id)
