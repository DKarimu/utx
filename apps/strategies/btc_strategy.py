from datetime import datetime, timedelta

import pandas as pd
from indexes import Indexes
from logger_util import UtxLogger as log
from models.order import Order
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

        if is_buy:
            trade_action = "BUY"
        else:
            trade_action = "SELL"

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
        return data

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
        rolling_mean, upper_band, lower_band = self.indexs.calculate_bollinger_bands(
            rates
        )
        normalized_rsi = self.indexs.calculate_rsi(rates)
        volatility = self.indexs.calculate_price_volatility(rates)

        # Determine trade action based on the rolling mean, current price, and state
        is_buy = rolling_mean.iloc[-1] < current_price
        is_sell = rolling_mean.iloc[-1] > current_price

        if is_buy:
            trade_action = "BUY"
        else:
            trade_action = "SELL"

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
        self.uti.export_to_csv(data, "BtcStraTesting.csv")
        return data

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

    def create_order_simulation(self):
        last_order = Order.objects.order_by("-created_at").first()
        strategy_result = self.execute_strategy()
        trade_action = strategy_result.get("TradeAction")[0]
        current_price = strategy_result.get("CurrentPrice")[0]

        self.log.info(
            "create_order_simulation",
            f"last_order: {last_order}, trade_action: {trade_action}",
        )

        if last_order is not None:
            if last_order.order_type == "BUY" and trade_action == "SELL":
                new_order_type = "SELL"
            elif last_order.order_type == "SELL" and trade_action == "BUY":
                new_order_type = "BUY"
            else:
                return
            new_order = Order(
                order_type=new_order_type,
                rate=current_price,
                id="utx_simulation",
                amount="0.05",
                time_in_force="utx_simulation",
                stop_loss_rate=None,
                pair="btc_jpy",
            )
            new_order.save()

        else:
            new_order_type = trade_action
            new_order = Order(
                order_type=new_order_type,
                rate=current_price,
                id="utx_simulation",
                amount="0.05",
                time_in_force="utx_simulation",
                stop_loss_rate=None,
                pair="btc_jpy",
            )
            new_order.save()
