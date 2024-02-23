from django.test import TestCase
from models.order import Order


class OrderModelTest(TestCase):

    def test_order_creation(self):
        # Create an Order instance
        order = Order.objects.create(
            success=True,
            order_id="123456",
            rate=100.00,
            amount=2.00,
            order_type="Market",
            time_in_force="GTC",
            stop_loss_rate=95.00,
            pair="BTC/USD",
        )

        # Check if the Order instance was created successfully
        self.assertTrue(isinstance(order, Order))

        # Check if the Order fields were saved correctly
        self.assertEqual(order.success, True)
        self.assertEqual(order.id, "123456")
        self.assertEqual(order.rate, 100.00)
        self.assertEqual(order.amount, 2.00)
        self.assertEqual(order.order_type, "Market")
        self.assertEqual(order.time_in_force, "GTC")
        self.assertEqual(order.stop_loss_rate, 95.00)
        self.assertEqual(order.pair, "BTC/USD")
