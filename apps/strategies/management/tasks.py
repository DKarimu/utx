# /app/apps/strategies/management/tasks.py
import inspect

from coincheck_client import CoincheckClient
from models.ticker import Ticker
from models.trade import Trade
from utx_logger import UtxLogger as log


class Tasks:
    def __init__(self):
        self.log = log(self.__class__.__name__)
        self.coincheck = CoincheckClient()

    def run_tasks(self):
        method_name = inspect.currentframe().f_back.f_code.co_name
        try:
            self.log.info(method_name, "Fetching tasks to run")
            self.create_ticker_data()
            self.create_trades_data()

        except Exception as e:
            self.log.error(method_name, f"Error in run_tasks: {str(e)}")

    def create_ticker_data(self):
        try:
            Ticker.create_ticker_data(self.coincheck.get_ticker())
        except Exception as e:
            self.log.error("create_ticker_data", f"Error: {str(e)}")

    def create_trades_data(self):
        try:
            Trade.create_trades_data(self.coincheck.get_public_trades())
        except Exception as e:
            self.log.error("create_trades_data", f"Error: {str(e)}")
