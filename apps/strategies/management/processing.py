# myapp/management/commands/batch_processing.py
import time

import requests
from django.core.management.base import BaseCommand
from utx_logger import UtxLogger as log

from apps.brokers.coincheck_client import CoincheckClient
from apps.data.models.market_data import Market


class Command(BaseCommand):
    help = "Run batch processing to fetch data from multiple APIs"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Batch processing started..."))
        coincheck = CoincheckClient()
        self.log = log(self.__class__.__name__)

        while True:
            try:
                res = Market.create_market_data(coincheck.get_ticker())
                self.log.info(self.__name__, res)

                self.stdout.write(
                    self.style.SUCCESS(
                        "Batch processing completed. Sleeping for 60 seconds..."
                    )
                )
                time.sleep(60)

            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Error during batch processing: {str(e)}")
                )
                time.sleep(60)
