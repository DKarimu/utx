import os
from datetime import datetime, timedelta

import pandas as pd
from indexes import Indexes
from logger_util import UtxLogger as log
from models.trade import Trade
from util import UtxUtils as uti

from apps.strategies.config import StrategiesConfig


def log_method_call(method):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.log.info(method.__name__, f"Executing method")
        return method(*args, **kwargs)

    return wrapper


class BTCStrategy:
    def __init__(self, config: StrategiesConfig = StrategiesConfig()):
        self.config = config
        self.indexs = Indexes()
        self.uti = uti()
        self.ready_to_buy = True
        self.log = log(self.__class__.__name__)

    def execute_strategy(self):
        trades = Trade.objects.all().order_by("-created_at")[:200]
        rates = pd.Series([float(trade.rate) for trade in trades])
        current_price = rates.iloc[0]
        maw = self.config.moving_average_window
        sdm = self.config.std_dev_multiplier
        rsi_period = self.config.rsi_period
        rolling_mean, upper_band, lower_band = self.indexs.calculate_bollinger_bands(
            rates, maw, sdm
        )
        normalized_rsi = self.indexs.calculate_rsi(rates, rsi_period)
        volatility = self.indexs.calculate_price_volatility(rates)

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
            "DateTime": [trades[199].utx_id],
            "CurrentPrice": [current_price],
            "RollingMean": [rolling_mean.iloc[-1]],
            "UpperBand": [upper_band.iloc[-1]],
            "LowerBand": [lower_band.iloc[-1]],
            "NormalizedRSI": [normalized_rsi.iloc[-1]],
            "Volatility": [volatility],
            "TradeAction": [trade_action],
        }
        self.uti.export_to_csv(data, "BtcStraTesting.csv")

    def load_and_apply_strategy(self, start_date, end_date):
        # Convert start_date and end_date to datetime objects
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # Filter trades within the given date range and order by creation time
        trades = Trade.objects.filter(
            created_at__range=(start_datetime, end_datetime)
        ).order_by("-created_at")[:200]

        if len(trades) == 0:
            self.log.info(
                "load_and_apply_strategy",
                "No trades found in the specified date range.",
            )
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
                trades[19].created_at if len(trades) >= 20 else trades[-1].created_at
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
        self.uti.export_to_csv(data)

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
