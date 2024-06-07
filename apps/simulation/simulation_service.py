from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from db_util import UtxDBService
from models.ticker import Ticker


class SimulationService:
    """
    A class to generate simulated financial data.
    """

    def __init__(self, start_price, days, volatility):
        """
        Initialize the simulation data generator.

        Args:
            start_price (float): The initial price of the asset.
            days (int): The number of data points to generate.
            volatility (float): The standard deviation of the price changes.
        """
        self.start_price = start_price
        self.days = days
        self.volatility = volatility
        UtxDBService().create_models_tables()

    def generate_data(self):
        """
        Generate the simulated financial data.

        Returns:
            list: A list of dictionaries containing simulated financial data.
        """
        # Generate timestamps
        current_time = datetime.now()
        timestamps = [
            int((current_time + timedelta(minutes=i)).timestamp())
            for i in range(self.days)
        ]

        # Generate random price changes based on normal distribution
        price_changes = np.random.normal(loc=0, scale=self.volatility, size=self.days)
        last_prices = self.start_price + np.cumsum(price_changes)
        last_prices = np.maximum(last_prices, 0)  # Ensure no negative prices

        # Generate bid, ask, high, and low prices with random adjustments
        bids = last_prices - np.random.uniform(0.01, 0.05, size=self.days)
        asks = last_prices + np.random.uniform(0.01, 0.05, size=self.days)
        highs = last_prices + np.random.uniform(0.05, 0.1, size=self.days)
        lows = last_prices - np.random.uniform(0.05, 0.1, size=self.days)
        lows = np.maximum(lows, 0)  # Ensure no negative prices

        # Generate random volumes
        volumes = np.random.uniform(10, 100, size=self.days)

        # Compile the generated data into a list of dictionaries
        data = []
        for i in range(self.days):
            record = {
                "last": round(last_prices[i], 2),
                "bid": round(bids[i], 2),
                "ask": round(asks[i], 2),
                "high": round(highs[i], 2),
                "low": round(lows[i], 2),
                "volume": f"{volumes[i]:.8f}",
                "timestamp": timestamps[i],
            }
            Ticker.create_ticker_data(record, True)
            data.append(record)
        return data


# Example usage:
# generator = SimulationDataGenerator(start_price=100, days=10, volatility=1)
# simulation_data = generator.generate_data()
# print(simulation_data)
