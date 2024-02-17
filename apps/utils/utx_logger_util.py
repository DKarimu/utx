import logging


class UtxLogger:
    def __init__(self, class_name):
        self.log = logging.getLogger(f"django.utx.{class_name}")

    def _log_message(self, method_name, msg, level):
        """Log a message with a specific level."""
        self.log.log(
            level, msg, extra={"class_name": self.log.name, "method_name": method_name}
        )

    def error(self, method_name, msg):
        """Log an error message."""
        self._log_message(method_name, msg, logging.ERROR)

    def warning(self, method_name, msg):
        """Log a warning message."""
        self._log_message(method_name, msg, logging.WARNING)

    def info(self, method_name, msg):
        """Log an info message."""
        self._log_message(method_name, msg, logging.INFO)

    def debug(self, method_name, msg):
        """Log a debug message."""
        self._log_message(method_name, msg, logging.DEBUG)

    def handle_request_error(
        self, error, status_code=None, method_name="unknown_method", response_text=None
    ):
        """Handle an error from a request, logging it appropriately."""
        error_msg = f"{error}"
        if status_code:
            error_msg += f", Status code: {status_code}"
        if response_text:
            error_msg += f", Response text: {response_text}"

        self.log.error(
            error_msg, extra={"class_name": self.log.name, "method_name": method_name}
        )
        return {"error": error_msg}
