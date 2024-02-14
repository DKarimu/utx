import os
from dataclasses import dataclass
from datetime import datetime, timedelta

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
        self.ready_to_buy = True
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
        rolling_mean, upper_band, lower_band = self.calculate_bollinger_bands(rates)
        normalized_rsi = self.calculate_rsi(rates)
        volatility = self.calculate_price_volatility(rates)

        # Determine trade action based on the rolling mean, current price, and state
        is_buy = rolling_mean.iloc[-1] < current_price
        is_sell = rolling_mean.iloc[-1] > current_price

        if self.ready_to_buy and is_buy:
            trade_action = "BUY"
            self.ready_to_buy = False
        elif not self.ready_to_buy and is_sell:
            trade_action = "SELL"
            self.ready_to_buy = True
        else:
            trade_action = "HOLD"

        # The rest of your method remains unchanged
        data = {
            "From": [trades[0].utx_create_time],
            "To": [trades[199].utx_create_time],
            "CurrentPrice": [current_price],
            "RollingMean": [rolling_mean.iloc[-1]],
            "UpperBand": [upper_band.iloc[-1]],
            "LowerBand": [lower_band.iloc[-1]],
            "NormalizedRSI": [normalized_rsi.iloc[-1]],
            "Volatility": [volatility],
            "TradeAction": [trade_action],
        }
        self.export_to_csv(data)

    def load_and_apply_strategy(self, start_date, end_date):
        # Convert start_date and end_date to datetime objects
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # Filter trades within the given date range and order by creation time
        trades = Trade.objects.filter(
            created_at__range=(start_datetime, end_datetime)
        ).order_by("-created_at")[:200]

        if len(trades) == 0:
            print("No trades found in the specified date range.")
            return

        rates = pd.Series([float(trade.rate) for trade in trades])
        current_price = rates.iloc[0]
        rolling_mean, upper_band, lower_band = self.calculate_bollinger_bands(rates)
        normalized_rsi = self.calculate_rsi(rates)
        volatility = self.calculate_price_volatility(rates)

        # Determine trade action based on the rolling mean, current price, and state
        is_buy = rolling_mean.iloc[-1] < current_price
        is_sell = rolling_mean.iloc[-1] > current_price

        if self.ready_to_buy and is_buy:
            trade_action = "BUY"
            self.ready_to_buy = False
        elif not self.ready_to_buy and is_sell:
            trade_action = "SELL"
            self.ready_to_buy = True
        else:
            trade_action = "HOLD"

        # Prepare the data for export
        data = {
            "From": [
                trades[199].created_at if len(trades) >= 200 else trades[-1].created_at
            ],
            "To": [trades[0].created_at],
            "CurrentPrice": [current_price],
            "RollingMean": [rolling_mean.iloc[-1]],
            "UpperBand": [upper_band.iloc[-1]],
            "LowerBand": [lower_band.iloc[-1]],
            "NormalizedRSI": [normalized_rsi.iloc[-1]],
            "Volatility": [volatility],
            "TradeAction": [trade_action],
        }
        self.export_to_csv(data)

    def test_strategy_over_periods(self, start_date, end_date, period_days=None):
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        if period_days is None:
            period_days = (end_datetime - start_datetime).days

        current_start_datetime = start_datetime

        while current_start_datetime < end_datetime:
            current_end_datetime = current_start_datetime + timedelta(days=period_days)
            if current_end_datetime > end_datetime:
                current_end_datetime = end_datetime

            current_start_date_str = current_start_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            current_end_date_str = current_end_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Apply the strategy for the current period
            self.log.info(
                "test_strategy_over_periods",
                f"Applying strategy from {current_start_date_str} to {current_end_date_str}",
            )
            self.load_and_apply_strategy(current_start_date_str, current_end_date_str)

            # Move to the next period
            current_start_datetime = current_end_datetime

    def export_to_csv(self, data):
        df = pd.DataFrame(data)
        file_exists = os.path.isfile("btc_strategy_output.csv")
        with open("btc_strategy_output.csv", "a") as f:
            df.to_csv(f, header=not file_exists, index=False)
        self.log.info(
            "export_to_csv", "Strategy output appended to btc_strategy_output.csv"
        )
