# coincheck_client.py

import time
import hmac
import hashlib
import requests
import logging

from urllib.parse import urlencode
from config.broker_config import coincheck


class CoincheckClient:
    """
    document: https://coincheck.com/documents/exchange/api
        PAIR currency pair to trade.
        btc_jpy, etc_jpy, lsk_jpy, mona_jpy, plt_jpy, fnct_jpy, dai_jpy, wbtc_jpy.
    """

    def __init__(self):
        api_config = coincheck
        self.api_key = api_config.api_key
        self.secret_key = api_config.secret_key

        # Set up a logger for the class
        self.log = logging.getLogger("django." + self.__class__.__name__)

    def construct_request_url(self, request, pair=None, **kwargs):
        request_endpoint = coincheck.api_urls.get(request)

        if not request_endpoint:
            raise ValueError(f"Invalid request: {request}")

        if "{}" in request_endpoint and not pair:
            raise ValueError("Pair is required for this request.")

        formatted_endpoint = (
            request_endpoint.format(pair)
            if "{}" in request_endpoint
            else request_endpoint
        )

        pair_parameter = f"pair={pair}" if pair else ""
        parameters = (
            f"?{pair_parameter}&{urlencode(kwargs)}" if kwargs else f"?{pair_parameter}"
        )

        return f"{coincheck.base_url}{formatted_endpoint}{parameters}"

    def handle_request_error(
        self, error, status_code=None, method_name=None, response_text=None
    ):
        error_msg = (
            f"{error}, Status code: {status_code}, Response text: {response_text}"
            if status_code
            else str(error)
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
                method_name,
                f"Request successful {response} data[{len(response.json())}]",
            )
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            return self.handle_request_error(
                http_err, response.status_code, method_name, response.text
            )

        except requests.exceptions.RequestException as req_err:
            return self.handle_request_error(req_err, method_name=method_name)

    def private_request(self, request, **kwargs):
        """
        Make a private request to the exchange API.

        Parameters:
            :request: API endpoint.
            :kwargs: Request parameters.

        Returns:
        - Response from the API.
        """
        method_name = "private_request"
        try:
            request_url = self.construct_request_url(request, **kwargs)
            headers = self.create_header(request_url)

            # Choose the appropriate HTTP method
            if "get" in request:
                response = requests.get(request_url, headers=headers)
            elif "post" in request:
                response = requests.post(request_url, headers=headers)
            elif "delet" in request:
                response = requests.delete(request_url, headers=headers)
            else:
                raise ValueError(
                    "Invalid HTTP method. Supported methods: GET, POST, DELETE"
                )

            response.raise_for_status()  # Raises HTTPError for bad responses
            self.log_message(
                method_name,
                f"Request successful {response} data[{len(response.json())}]",
            )
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            return self.handle_request_error(
                http_err, response.status_code, method_name, response.text
            )

        except requests.exceptions.RequestException as req_err:
            return self.handle_request_error(req_err, method_name=method_name)

    def create_header(self, url):
        nonce = str(round(time.time() * 1000000))  # Nonce must be incremented
        signature = self.create_signature(url, nonce)
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-NONCE": nonce,
            "ACCESS-SIGNATURE": signature,
        }
        return headers

    def create_signature(self, url, nonce):
        message = nonce + url
        signature = self.hmac_sha256_encode(self.secret_key, message)
        return signature

    def hmac_sha256_encode(self, secret_key, message):
        secret_key = bytes(secret_key, "UTF-8")
        message = bytes(message, "UTF-8")
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        return signature

    # Public API
    # Public API allows you to browse order status, order transactions and order book.
    def get_ticker(self, pair="btc_jpy"):
        """
        Ticker
        Check the latest information for a specified pair.
        If pair is not specified, it defaults to btc_jpy.
            :param pair: Pair (e.g., "btc_jpy")

        Returns:
            :Result of the Ticker request.
        """
        method_name = "get_ticker"
        self.log_message(method_name, f"Fetching Ticker for pair: {pair}")
        return self.public_request(method_name, pair=pair)

    def get_trades(self, pair="btc_jpy"):
        """
        Public trades
        Get current order transactions for a specified pair.
        If pair is not specified, it defaults to btc_jpy.
            :param pair: Pair (e.g., "btc_jpy")

        Returns:
            :Result of the Public trades request.
        """
        method_name = "get_trades"
        self.log_message(method_name, f"Fetching Public trades for pair: {pair}")
        return self.public_request(method_name, pair=pair)

    def get_orderbooks(self):
        """
        Order Book
        Fetch order book information.

        Returns:
            :asks Sell order status
            :bids Buy order status
        """
        method_name = "get_orderbooks"
        self.log_message(method_name, "Fetching Order Book")
        return self.public_request(method_name)

    def get_calc_rate(self, pair, order_type, amount=None, price=None):
        """
        Calc Rate
        Calculate the rate from the order of the exchange.
            :param order_type: Order type ("sell" or "buy").
            :param pair: Pair (e.g., "btc_jpy").
            :param amount: Order amount (e.g., 0.1).
            :param price: Order price (e.g., 28000).
        ※Either price or amount must be specified as a parameter.

        Returns:
            :rate Order rate
            :price Order price
            :amount Order amount
        """
        method_name = "get_calc_rate"
        self.log_message(
            method_name,
            f"Fetching Calc Rate for pair: {pair}, order_type: {order_type}, amount: {amount},price: {price}",
        )
        parameters = {"pair": pair, "order_type": order_type}
        if amount is not None:
            parameters["amount"] = amount
        elif price is not None:
            parameters["price"] = price
        return self.public_request(method_name, **parameters)

    def get_standard_rate(self, pair="btc_jpy"):
        """
        Standard Rate
        Get the standard rate of the coin.
            :pair: Pair (e.g., "btc_jpy").

        Returns:
            :rate
        """
        method_name = "get_standard_rate"
        self.log_message(method_name, f"Fetching Standard Rate for pair: {pair}")
        return self.public_request(method_name, pair=pair)

    # Private API
    # Private API allows you to order, cancel new orders and make sure your balance.
    def post_new_order(
        self,
        pair,
        order_type,
        rate,
        amount,
        market_buy_amount=None,
        stop_loss_rate=None,
        time_in_force=None,
    ):
        """
        New order
        Publish a new order to the exchange.
        Parameters:
            :pair: Specify a currency pair to trade (e.g., btc_jpy).
            :order_type: Specify order_type ("buy", "sell", "market_buy", "market_sell").
            :rate: Order rate (e.g., 30000).
            :amount: Order amount (e.g., 10).
            :market_buy_amount: Market buy amount in JPY (required for market_buy).
            :stop_loss_rate: Stop Loss Rate (optional).
            :time_in_force: Time In Force (optional, default is "good_til_cancelled" or use "post_only").

        Returns:
            :Result of the new order request.
        """
        method_name = "post_new_order"
        # Build the request payload
        payload = {
            "pair": pair,
            "order_type": order_type,
            "rate": rate,
            "amount": amount,
            "market_buy_amount": market_buy_amount,
            "stop_loss_rate": stop_loss_rate,
            "time_in_force": time_in_force,
        }

        self.log_message(
            method_name, f"Placing new order for pair: {pair} Parameters {payload}"
        )

        return self.private_request(method_name, **payload)
