# coincheck_client.py

import logging
import requests
from config.broker_config import coincheck


class CoincheckClient:
    """
    document: https://coincheck.com/documents/exchange/api
    """

    def __init__(self):
        api_config = coincheck
        self.api_key = api_config.api_key
        self.secret_key = api_config.secret_key
        # Initialize any other necessary parameters

        # Use Django's logger
        self.log = logging.getLogger("django")

    def authenticate(self):
        # Implement authentication logic using the provided API key and secret key
        # Set up headers, authentication tokens, etc.
        self.log.info(f"Authenticated to Broker1 with account ID: ")

    def construct_request_url(self, request):
        request_endpoint = coincheck.api_urls[request]
        return f"{coincheck.base_url}{request_endpoint}"

    def public_request(self, request):
        request_url = self.construct_request_url(request)

        try:
            response = requests.get(request_url)
            response.raise_for_status()  # Raises HTTPError for bad responses

            return response.json()

        except requests.exceptions.HTTPError as http_err:
            self.log.error(
                f"HTTP error occurred: {http_err}, Status code: {response.status_code}"
            )
            return {
                "error": f"HTTP error: {http_err}, Status code: {response.status_code}"
            }

        except requests.exceptions.RequestException as req_err:
            self.log.error(f"Request error occurred: {req_err}")
            return {"error": f"Request error: {req_err}"}

    def ticker(self):
        self.log.info(f"request for ticker")
        return self.public_request("ticker")

    def trades(self):
        return self.public_request("trades")

    def orderbooks(self):
        return self.public_request("order_books")
