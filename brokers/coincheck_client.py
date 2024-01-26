import logging
import requests
from urllib.parse import urlencode
from config.broker_config import coincheck


class CoincheckClient:
    """
    document: https://coincheck.com/documents/exchange/api
    """

    def __init__(self):
        api_config = coincheck
        self.api_key = api_config.api_key
        self.secret_key = api_config.secret_key

        # Set up a logger for the class
        self.log = logging.getLogger("django." + self.__class__.__name__)

    def construct_request_url(self, request, **kwargs):
        request_endpoint = coincheck.api_urls.get(request)
        if not request_endpoint:
            raise ValueError(f"Invalid request: {request}")

        parameters = urlencode(kwargs) if kwargs else ""
        return f"{coincheck.base_url}{request_endpoint}?{parameters}"

    def handle_request_error(self, error, status_code=None, method_name=None):
        error_msg = (
            f"{error}, Status code: {status_code}" if status_code else str(error)
        )
        log_params = {
            "class_name": self.__class__.__name__,
            "method_name": method_name or "unknown_method",
        }
        self.log.error(error_msg, extra=log_params)
        return {"error": error_msg}

    def log_message(self, method_name, msg):
        self.log.info(
            msg,
            extra={"class_name": self.__class__.__name__, "method_name": method_name},
        )

    def public_request(self, request, **kwargs):
        method_name = "public_request"
        try:
            request_url = self.construct_request_url(request, **kwargs)
            response = requests.get(request_url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            self.log_message(
                method_name, f"Request successful{response} data {response.json()}"
            )
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            return self.handle_request_error(
                http_err, response.status_code, method_name
            )

        except requests.exceptions.RequestException as req_err:
            return self.handle_request_error(req_err, method_name=method_name)

    def ticker(self):
        method_name = "ticker"
        self.log_message(method_name, "Fetching ticker")
        return self.public_request("ticker")

    def trades(self, pair):
        method_name = "trades"
        self.log_message(method_name, "Fetching trades")
        parameters = {"pair": pair}
        return self.public_request("trades", **parameters)

    def orderbooks(self):
        method_name = "orderbooks"
        self.log_message(method_name, "Fetching order books")
        return self.public_request("order_books")
