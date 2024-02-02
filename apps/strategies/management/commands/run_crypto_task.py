# ./apps/strategies/management/commands/run_crypto_task.py
import time

from coincheck_client import CoincheckClient
from django.core.management.base import BaseCommand
from models.market_data import Market
from utx_logger import UtxLogger as log

from apps.strategies.crypto_strategie import CryptoStrategie


class Command(BaseCommand):
    help = "Run crypto strategies as a background task"

    def handle(self, *args, **options):
        CryptoStrategie()
        self.stdout.write(self.style.SUCCESS("Successfully ran crypto strategies."))
        coincheck = CoincheckClient()
        self.log = log(self.__class__.__name__)
        sleeping_seconds = 5

        while True:
            try:
                res = Market.create_market_data(coincheck.get_ticker())
                self.log.info("", res)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Batch processing completed. Sleeping for {sleeping_seconds} seconds..."
                    )
                )
                time.sleep(sleeping_seconds)

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error during batch processing: {str(e)}")
                )
                time.sleep(60)
