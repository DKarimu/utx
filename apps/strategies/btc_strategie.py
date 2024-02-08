# ./apps/strategies/btc_strategy.py
import numpy as np
import pandas as pd
from models.trade import Trade


# Function to calculate Bollinger Bands
def calculate_bollinger_bands(prices, window, num_of_std):
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, upper_band, lower_band


# Strategy Execution Function
def execute_btc_strategy():
    # Get trade data from the database
    trades = Trade.objects.all().order_by("-timestamp")[
        :200
    ]  # Assuming you have a timestamp field
    prices = np.array([trade.price for trade in trades])

    # Calculate Bollinger Bands
    rolling_mean, upper_band, lower_band = calculate_bollinger_bands(
        pd.Series(prices), window=20, num_of_std=2
    )

    # Assume that the latest price is the current price
    current_price = prices[0]
    # Generate buy/sell signals based on Bollinger Bands
    if current_price < lower_band[-1]:  # If current price breaks below lower band
        print("BUY SIGNAL")
        # Insert buy logic here
    elif current_price > upper_band[-1]:  # If current price breaks above upper band
        print("SELL SIGNAL")
        # Insert sell logic here
    else:
        print("NO CLEAR SIGNAL")
        # No action is taken

    # ... rest of your strategy logic ...


# Don't forget to handle errors and edge cases in your actual implementation
