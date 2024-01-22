# myapp/management/commands/batch_processing.py
import time
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Run batch processing to fetch data from multiple APIs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Batch processing started...'))

        while True:
            try:
                # Fetch data from API 1
                api1_data = requests.get('https://api1.example.com').json()

                # Fetch data from API 2
                api2_data = requests.get('https://api2.example.com').json()

                # Process data as needed
                # ...

                self.stdout.write(self.style.SUCCESS('Batch processing completed. Sleeping for 60 seconds...'))
                time.sleep(60)  # Sleep for 60 seconds before the next iteration

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error during batch processing: {str(e)}'))
                time.sleep(60)  # Sleep for 60 seconds even if an error occurs
