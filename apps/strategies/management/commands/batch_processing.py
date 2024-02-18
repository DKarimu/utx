import signal
import time

from db_util import UtxDBService
from django.core.management.base import BaseCommand
from logger_util import UtxLogger as log
from management.tasks import Tasks


class Command(BaseCommand):
    help = "Run strategies as a background task"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sleeping_seconds",
            type=int,
            default=5,
            help="Number of seconds to sleep between iterations",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running = True
        self.log = log(self.__class__.__name__)
        self.tasks = Tasks()
        UtxDBService().create_models_tables()

    def handle(self, *args, **options):
        signal.signal(signal.SIGINT, self.handle_interrupt)
        self.stdout.write(self.style.SUCCESS("Successfully started batch processing."))

        sleeping_seconds = options["sleeping_seconds"]
        while self._running:
            self.execute_tasks(sleeping_seconds)

    def execute_tasks(self, sleeping_seconds):
        try:
            self.tasks.run_all_tasks()
            self.log_info(
                f"Batch processing completed. Sleeping for {sleeping_seconds} seconds..."
            )
            time.sleep(sleeping_seconds)

        except Exception as e:
            self.handle_exception(e)

    def log_info(self, message):
        self.log.info(self.__class__.__name__, message)

    def handle_exception(self, e):
        sleeping_seconds_on_error = 60
        msg = f"Error during batch processing: {str(e)}.Sleeping for {sleeping_seconds_on_error} seconds..."
        self.stderr.write(self.style.ERROR(msg))
        self.log.error(self.__class__.__name__, msg)
        time.sleep(60)

    def handle_interrupt(self, signum, frame):
        self._prompt_to_continue()

    def _prompt_to_continue(self):
        self.stdout.write(self.style.SUCCESS("Received interrupt signal."))
        user_input = input("Do you want to continue (y/n)? ").lower()
        if user_input == "n":
            self._running = False
            self.stdout.write(self.style.SUCCESS("Batch processing stopped by user."))
        elif user_input != "y":
            self.stdout.write(
                self.style.WARNING("Invalid input. Continuing batch processing.")
            )
