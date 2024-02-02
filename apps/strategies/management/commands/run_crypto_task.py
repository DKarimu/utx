# ./apps/strategies/management/commands/run_crypto_task.py

from django.core.management.base import BaseCommand

from apps.strategies.crypto_strategie import CryptoStrategie


class Command(BaseCommand):
    help = "Run crypto strategies as a background task"

    def handle(self, *args, **options):
        CryptoStrategie()
        self.stdout.write(self.style.SUCCESS("Successfully ran crypto strategies."))
