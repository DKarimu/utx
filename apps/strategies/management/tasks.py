from coincheck_client import CoincheckClient
from models.ticker import Ticker
from models.trade import Trade
from utx_logger import UtxLogger as log


def log_task(method):
    def wrapper(self, *args, **kwargs):
        self.log.info(f"{method.__name__}", "Starting task")
        try:
            result = method(self, *args, **kwargs)
            self.log.info(f"{method.__name__}", "Task completed successfully")
            return result
        except Exception as e:
            self.log.error(f"{method.__name__}", f"Error: {str(e)}")
            raise e

    return wrapper


class Tasks:
    def __init__(self):
        self.log = log(self.__class__.__name__)
        self.coincheck = CoincheckClient()

    def run_tasks(self):
        try:
            self.create_ticker_data()
            self.create_trades_data()
        except Exception as e:
            # General error handling if needed
            pass

    @log_task
    def create_ticker_data(self):
        res = self.coincheck.get_ticker()
        Ticker.create_ticker_data(res)

    @log_task
    def create_trades_data(self):
        res = self.coincheck.get_public_trades()
        Trade.create_trades_data(res)
