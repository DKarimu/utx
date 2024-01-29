import logging


class UtxLogger:
    def __init__(self, class_name):
        self.log = logging.getLogger("django." + class_name)

    def log_message(self, method_name, msg, level=logging.INFO):
        self.log.log(
            level,
            msg,
            extra={"class_name": self.log.name, "method_name": method_name},
        )

    def error(self, method_name, msg):
        self.log_message(method_name, msg, level=logging.ERROR)

    def warning(self, method_name, msg):
        self.log_message(method_name, msg, level=logging.WARNING)

    def info(self, method_name, msg):
        self.log_message(method_name, msg, level=logging.INFO)

    def debug(self, method_name, msg):
        self.log_message(method_name, msg, level=logging.DEBUG)

    def handle_request_error(
        self, error, status_code=None, method_name=None, response_text=None
    ):
        error_msg = (
            f"{error}, Status code: {status_code}, Response text: {response_text}"
            if status_code
            else str(error)
        )
        log_params = {
            "class_name": self.log.name,
            "method_name": method_name or "unknown_method",
        }
        self.log.error(error_msg, extra=log_params)
        return {"error": error_msg}
