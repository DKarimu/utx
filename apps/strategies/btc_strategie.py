import os
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from models.trade import Trade
from utx_logger import UtxLogger as log


@dataclass
class StrategyConfig:
    moving_average_window: int = 20
    std_dev_multiplier: int = 2
    rsi_period: int = 14


def log_method_call(method):
    def wrapper(*args, **kwargs):
        self = args[0]
        kwargs_str = (
            ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else "***"
        )
        self.log.info(method.__name__, f"Executing method with kwargs: {kwargs_str}")
        return method(*args, **kwargs)

    return wrapper


class BTCStrategy:
    def __init__(self, config: StrategyConfig = StrategyConfig()):
        self.config = config
        self.log = log(self.__class__.__name__)

    @log_method_call
    def calculate_bollinger_bands(self, rates):
        rolling_mean = rates.rolling(window=self.config.moving_average_window).mean()
        rolling_std = rates.rolling(window=self.config.moving_average_window).std()
        upper_band = rolling_mean + (rolling_std * self.config.std_dev_multiplier)
        lower_band = rolling_mean - (rolling_std * self.config.std_dev_multiplier)
        return rolling_mean, upper_band, lower_band

    @log_method_call
    def calculate_rsi(self, rates):
        delta = rates.diff().dropna()
        gain = delta.where(delta > 0, 0).rolling(window=self.config.rsi_period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=self.config.rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        normalized_rsi = (rsi - 50) * 0.02
        return normalized_rsi

    @log_method_call
    def calculate_price_volatility(self, rates):
        volatility = rates.std()
        return volatility

    def execute_strategy(self):
        trades = Trade.objects.all().order_by("-created_at")[:200]
        rates = pd.Series([float(trade.rate) for trade in trades])
        current_price = rates.iloc[0]
        current_time = datetime.now().time()
        rolling_mean, upper_band, lower_band = self.calculate_bollinger_bands(rates)
        normalized_rsi = self.calculate_rsi(rates)
        volatility = self.calculate_price_volatility(rates)

        # Organize data into a dictionary for DataFrame creation
        data = {
            "TIME": [current_time],
            "CurrentPrice": [current_price],
            "RollingMean": [rolling_mean.iloc[-1]],
            "UpperBand": [upper_band.iloc[-1]],
            "LowerBand": [lower_band.iloc[-1]],
            "NormalizedRSI": [normalized_rsi.iloc[-1]],
            "Volatility": [volatility],
        }
        self.export_to_csv(data)

    def export_to_csv(self, data):
        df = pd.DataFrame(data)
        file_exists = os.path.isfile("btc_strategy_output.csv")
        with open("btc_strategy_output.csv", "a") as f:
            df.to_csv(f, header=not file_exists, index=False)
        self.log.info(
            "export_to_csv", "Strategy output appended to btc_strategy_output.csv"
        )
