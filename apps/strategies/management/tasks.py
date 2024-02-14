import inspect

from btc_strategie import BTCStrategy
from coincheck_client import CoincheckClient
from models.ticker import Ticker
from models.trade import Trade
from utx_logger import UtxLogger as log


def log_task(method):
    def wrapper(task, *args, **kwargs):
        task.log.info(f"{method.__name__}", "Starting task")
        try:
            result = method(task, *args, **kwargs)
            task.log.info(f"{method.__name__}", "Task completed successfully")
            return result
        except Exception as e:
            task.log.error(f"{method.__name__}", f"Error: {str(e)}")
            pass

    return wrapper


class Tasks:
    def __init__(self):
        self.log = log(self.__class__.__name__)
        self.coincheck = CoincheckClient()

    def run_all_tasks(self):
        this_method = "run_all_tasks"
        method_names = [
            method_name
            for method_name in dir(self)
            if callable(getattr(self, method_name)) and not method_name.startswith("_")
        ]
        for method_name in method_names:
            method = getattr(self, method_name)
            if method_name != this_method:
                try:
                    method()
                except Exception as e:
                    self.log.error(f"{method_name}", f"Error: {str(e)}")
                    pass

    # @log_task
    # def create_ticker_data(self):
    #     res = self.coincheck.get_ticker()
    #     Ticker.create_ticker_data(res)

    # @log_task
    # def create_trades_data(self):
    #     res = self.coincheck.get_public_trades()
    #     Trade.create_trades_data(res)

    @log_task
    def run_strategies(self):
        btcs = BTCStrategy()
        btcs.load_and_apply_strategy()
        # btcs.execute_strategy()

    # add more task methods here
