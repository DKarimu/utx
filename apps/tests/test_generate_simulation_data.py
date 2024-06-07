import unittest

from models.ticker import Ticker

from apps.simulation.simulation_service import SimulationService


class TestSimulationDataGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, if any."""
        self.start_price = 100
        self.days = 10
        self.volatility = 1
        self.generator = SimulationService(self.start_price, self.days, self.volatility)

    def test_generate_data(self):
        """Test the generate_data method of SimulationDataGenerator."""
        result = self.generator.generate_data()

        # Ensure the result is a list
        self.assertIsInstance(result, list)

        # Ensure each item in the result list is a dictionary with the correct keys
        for record in result:
            self.assertIsInstance(record, dict)
            self.assertIn("last", record)
            self.assertIn("bid", record)
            self.assertIn("ask", record)
            self.assertIn("high", record)
            self.assertIn("low", record)
            self.assertIn("volume", record)
            self.assertIn("timestamp", record)

            Ticker.create_ticker_data(record)

        # Ensure the correct number of data points is generated
        self.assertEqual(len(result), self.days)

    def test_volatility_impact(self):
        """Test that increasing volatility increases price variation."""
        high_volatility_generator = SimulationService(
            self.start_price, self.days, 10 * self.volatility
        )
        low_volatility_generator = SimulationService(
            self.start_price, self.days, self.volatility / 10
        )

        high_volatility_result = high_volatility_generator.generate_data()
        low_volatility_result = low_volatility_generator.generate_data()

        high_volatility_prices = [record["last"] for record in high_volatility_result]
        low_volatility_prices = [record["last"] for record in low_volatility_result]

        high_volatility_range = max(high_volatility_prices) - min(
            high_volatility_prices
        )
        low_volatility_range = max(low_volatility_prices) - min(low_volatility_prices)

        self.assertGreater(high_volatility_range, low_volatility_range)


if __name__ == "__main__":
    unittest.main()
