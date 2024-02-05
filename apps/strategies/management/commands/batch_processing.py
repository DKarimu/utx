# /app/apps/strategies/management/commands/batch_processing.py
# python manage.py batch_processing --sleeping_seconds=10

import inspect
import signal
import time
from argparse import ArgumentParser  # Import ArgumentParser

from coincheck_client import CoincheckClient
from django.core.management.base import BaseCommand
from models.orderbook import OrderBook
from models.ticker import Ticker
from models.trade import Trade
from utx_db_service import UtxDBService
from utx_logger import UtxLogger as log


class Command(BaseCommand):
    help = "Run strategies as a background task"

    def add_arguments(self, parser):  # Add this method to handle command-line arguments
        parser.add_argument(
            "--sleeping_seconds",
            type=int,
            default=5,
            help="Number of seconds to sleep between iterations",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running = True

    def handle(self, *args, **options):
        method_name = inspect.currentframe().f_back.f_code.co_name
        UtxDBService().create_models_tables()
        signal.signal(signal.SIGINT, self.handle_interrupt)
        self.stdout.write(self.style.SUCCESS("Successfully ran strategies."))
        coincheck = CoincheckClient()
        self.log = log(self.__class__.__name__)

        # Retrieve sleeping_seconds from command-line arguments
        sleeping_seconds = options["sleeping_seconds"]

        while self._running:
            try:
                Ticker.create_ticker_data(coincheck.get_ticker())
                Trade.create_trades_data(coincheck.get_public_trades())
                res = coincheck.get_orderbooks()
                OrderBook.create_order_book(res)
                self.log.info(
                    method_name,
                    f"Batch processing completed. Sleeping for {sleeping_seconds} seconds...",
                )
                time.sleep(sleeping_seconds)

            except KeyboardInterrupt:
                user_input = input("Do you want to continue (y/n)? ").lower()
                if user_input == "n":
                    self._running = False
                    self.stdout.write(
                        self.style.SUCCESS("Batch processing stopped by user.")
                    )
                elif user_input != "y":
                    self.stdout.write(
                        self.style.WARNING(
                            "Invalid input. Continuing batch processing."
                        )
                    )

            except Exception as e:
                msg = f"Error during batch processing: {str(e)}"
                self.stderr.write(self.style.ERROR(msg))
                self.log.error(method_name, msg)
                time.sleep(60)

    def handle_interrupt(self, signum, frame):
        self.stdout.write(self.style.SUCCESS("Received interrupt signal."))
        user_input = input("Do you want to continue (y/n)? ").lower()
        if user_input == "n":
            self._running = False
            self.stdout.write(self.style.SUCCESS("Batch processing stopped by user."))
        elif user_input != "y":
            self.stdout.write(
                self.style.WARNING("Invalid input. Continuing batch processing.")
            )
