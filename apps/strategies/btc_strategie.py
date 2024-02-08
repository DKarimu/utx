import inspect

import numpy as np
import pandas as pd
from models.trade import Trade
from utx_logger import UtxLogger as log


class BTCStrategy:
    def __init__(self, window=20, num_of_std=2):
        self.window = window
        self.num_of_std = num_of_std
        self.log = log(self.__class__.__name__)  # Initialize the logger

    def get_method_name(self):
        return inspect.currentframe().f_back.f_code.co_name

    def calculate_bollinger_bands(self, rates):
        method_name = self.get_method_name()
        self.log.info(method_name, "Calculating Bollinger Bands")
        rolling_mean = rates.rolling(window=self.window).mean()
        rolling_std = rates.rolling(window=self.window).std()
        upper_band = rolling_mean + (rolling_std * self.num_of_std)
        lower_band = rolling_mean - (rolling_std * self.num_of_std)

        return rolling_mean, upper_band, lower_band

    def execute_strategy(self):
        method_name = self.get_method_name()
        self.log.info(method_name, "Executing BTC Strategy")  # Example log message
        # Get trade data from the database
        trades = Trade.objects.all().order_by("-created_at")[:60]
        rates = pd.Series(
            [float(trade.rate) for trade in trades]
        )  # Ensure rates are floats

        # Calculate Bollinger Bands
        rolling_mean, upper_band, lower_band = self.calculate_bollinger_bands(rates)

        # Assume that the latest rate is the current rate
        current_price = rates.iloc[0]  # Use iloc to ensure consistency with Pandas

        # Generate buy/sell signals based on Bollinger Bands
        if current_price < lower_band.iloc[-1]:  # Ensure comparison is between floats
            self.log.info(method_name, f"BUY SIGNAL current_price [{current_price}]")
            # Insert buy logic here
        elif current_price > upper_band.iloc[-1]:  # Ensure comparison is between floats
            self.log.info(method_name, f"SELL SIGNAL current_price [{current_price}]")
            # Insert sell logic here
        else:
            self.log.info(method_name, "NO CLEAR SIGNAL")
            # No action is taken


# Don't forget to handle errors and edge cases in your actual implementation
