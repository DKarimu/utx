# coincheck_client.py

import hashlib
import hmac
import inspect
import time
from urllib.parse import urlencode

import requests
from config.brokers_config import coincheck_cfg
from utx_logger import UtxLogger as log


class CoincheckClient:
    """
    document: https://coincheck.com/documents/exchange/api
        PAIR currency pair to trade.
        btc_jpy, etc_jpy, lsk_jpy, mona_jpy, plt_jpy, fnct_jpy, dai_jpy, wbtc_jpy.
    """

    def __init__(self):
        api_config = coincheck_cfg
        self.api_key = api_config.api_key
        self.secret_key = api_config.secret_key
        self.log = log(self.__class__.__name__)

    def get_method_name(self):
        return inspect.currentframe().f_back.f_code.co_name

    def construct_request_url(self, request, pair=None, id=None, **kwargs):
        request_endpoint = coincheck_cfg.api_urls.get(request)

        if not request_endpoint:
            return ValueError(f"Invalid request: {request}")

        if "{}" in request_endpoint and not (pair or id):
            return ValueError("Pair is required for this request.")

        formatted_endpoint = (
            request_endpoint.format(pair or id)
            if "{}" in request_endpoint and (pair or id)
            else request_endpoint
        )
        param = f"id={id}" if id else f"pair={pair}" if pair else ""
        parameters = (
            f"?{param}&{urlencode(kwargs)}"
            if param or kwargs
            else f"?{param}"
            if param
            else ""
        )
        return f"{coincheck_cfg.base_url}{formatted_endpoint}{parameters}"

    def public_request(self, request, **kwargs):
        method_name = self.get_method_name()
        try:
            request_url = self.construct_request_url(request, **kwargs)
            response = requests.get(request_url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            self.log.info(
                method_name,
                f"{request_url} Request successful {response} data[{len(response.json())}]",
            )
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return self.log.handle_request_error(
                http_err, response.status_code, method_name, response.text
            )
        except requests.exceptions.RequestException as req_err:
            return self.log.handle_request_error(req_err, method_name=method_name)

    def private_request(self, request, **kwargs):
        """
        Make a private request to the exchange API.

        Parameters:
            :request: API endpoint.
            :kwargs: Request parameters.

        Returns:
        - Response from the API.
        """
        method_name = self.get_method_name()
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
                return ValueError(
                    "Invalid HTTP method. Supported methods: GET, POST, DELETE"
                )
            response.raise_for_status()  # Raises HTTPError for bad responses
            self.log.info(
                method_name,
                f"{request_url} Request successful {response} data[{len(response.json())}]",
            )
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            return self.log.handle_request_error(
                http_err, response.status_code, method_name, response.text
            )

        except requests.exceptions.RequestException as req_err:
            return self.log.handle_request_error(req_err, method_name=method_name)

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

        Parameters:
            :param pair Pair (e.g., "btc_jpy")
        Return:
            :Result of the Ticker request.
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Ticker for pair: {pair}")
        return self.public_request(method_name, pair=pair)

    def get_trades(self, pair="btc_jpy"):
        """
        Public trades
        Get current order transactions for a specified pair.
        If pair is not specified, it defaults to btc_jpy.

        Parameters:
            :param pair Pair (e.g., "btc_jpy")
        Return:
            :Result of the Public trades request.
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Public trades for pair: {pair}")
        return self.public_request(method_name, pair=pair)

    def get_orderbooks(self):
        """
        Order Book
        Fetch order book information.

        Returns:
            :asks Sell order status
            :bids Buy order status
        """
        method_name = self.get_method_name()
        self.log.info(method_name, "Fetching Order Book")
        return self.public_request(method_name)

    def get_calc_rate(self, pair, order_type, amount="", price=""):
        """
        Calc Rate
        Calculate the rate from the order of the exchange.

        Parameters:
            :param order_type Order type ("sell" or "buy").
            :param pair Pair (e.g., "btc_jpy").
            :param amount Order amount (e.g., 0.1).
            :param price Order price (e.g., 28000).
        ※Either price or amount must be specified as a parameter.
        Returns:
            :rate Order rate
            :price Order price
            :amount Order amount
        """
        method_name = self.get_method_name()
        self.log.info(
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

        Parameters:
            :pair Pair (e.g., "btc_jpy").
        Return:
            :rate
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Standard Rate for pair: {pair}")
        return self.public_request(method_name, pair=pair)

    # Private API
    # Private API allows you to order, cancel new orders and make sure your balance.
    def post_new_order(
        self,
        pair,
        order_type,
        rate,
        amount,
        market_buy_amount="",
        stop_loss_rate="",
        time_in_force="",
    ):
        """
        New order
        Publish a new order to the exchange.

        Parameters:
            :pair Specify a currency pair to trade (e.g., btc_jpy).
            :order_type Specify order_type ("buy", "sell", "market_buy", "market_sell").
            :rate Order rate (e.g., 30000).
            :amount Order amount (e.g., 10).
            :market_buy_amount Market buy amount in JPY (required for market_buy).
            :stop_loss_rate Stop Loss Rate (optional).
            :time_in_force Time In Force (optional, default is "good_til_cancelled" or use "post_only").
        Returns:
            :Result of the new order request.
        """
        method_name = self.get_method_name()
        payload = {
            "pair": pair,
            "order_type": order_type,
            "rate": rate,
            "amount": amount,
            "market_buy_amount": market_buy_amount,
            "stop_loss_rate": stop_loss_rate,
            "time_in_force": time_in_force,
        }
        self.log.info(method_name, f"Placing new order for Parameters {payload}")
        return self.private_request(method_name, **payload)

    def get_unsettled_order_list(self):
        """
        Unsettled order list
        You can get a unsettled order list.

        Returns:
            :id Order ID(It's the same ID in New order.)
            :rate Order rate ( Market order if null)
            :pending_amount Unsettle order amount
            :pending_market_buy_amount Unsettled order amount (only for spot market buy order)
            :order_type order type("sell" or "buy")
            :stop_loss_rate Stop Loss Order's Rate
            :pair Deal pair
            :created_at Order date
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Unsettled order list")
        return self.private_request(method_name)

    def delet_cancel_order(self, id):
        """
        Cancel Order
        New Order, Or you can cancel by specifying unsettle order list's ID.

        Parameters:
            :id New order or Unsettle order list's ID
        Return:
            :id Canceled order ID
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Delet New Order or nsettle order id: {id}")
        return self.private_request(method_name, id=id)

    def get_order_cancellation_status(self, id):
        """
        Order cancellation status
        You can refer to the cancellation processing status of the order.

        Parameters:
            :id New order or Unsettle order list's ID
        Returns:
            :id Canceled order ID
            :cancel Canceled
            :created_at Ordered time
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Order cancellation status id: {id}")
        return self.private_request(method_name, id=id)

    def get_transaction_history(self):
        """
        Transaction history
        Display your transaction history

        Returns:
            :id ID
            :order_id Order ID
            :created_at Ordered time
            :funds Each fund balance's increase and decrease
            :pair Pair
            :rate Rate
            :fee_currency Fee currency
            :fee Fee amount
            :liquidity "T" ( Taker ) or "M" ( Maker )
            :side "sell" or "buy"
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Transaction history")
        return self.private_request(method_name)

    def get_transaction_history_pagination(self):
        """
        Transaction history (Pagination)
        Display your transaction history

        Returns:
            :id ID
            :order_id Order ID
            :created_at Ordered time
            :funds Each fund balance's increase and decrease
            :pair Pair
            :rate Rate
            :fee_currency Fee currency
            :fee Fee amount
            :liquidity "T" ( Taker ) or "M" ( Maker )
            :side "sell" or "buy"
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Transaction history (Pagination)")
        return self.private_request(method_name)

    # Account
    # You can get balance and various information.
    def get_balance(self):
        """
        Balance
        Check your account balance.

        Returns:
            :jpy Balance for JPY
            :btc Balance for BTC
            :jpy_reserved Amount of JPY for unsettled buying order
            :btc_reserved Amount of BTC for unsettled selling order
            :jpy_lend_in_use JPY amount you are applying for lending (We don't allow you to loan JPY.)
            :btc_lend_in_use BTC Amount you are applying for lending (We don't allow you to loan BTC.)
            :jpy_lent JPY lending amount (Currently, we don't allow you to loan JPY.)
            :btc_lent BTC lending amount (Currently, we don't allow you to loan BTC.)
            :jpy_debt JPY borrowing amount
            :btc_debt BTC borrowing amount
            :jpy_tsumitate JPY reserving amount
            :btc_tsumitate BTC reserving amount
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Balance")
        return self.private_request(method_name)

    def get_send_crypto_currency(
        self, remittee_list_id, amount, purpose_type, purpose_details
    ):
        """
        Send Crypto Currency
        Sending Crypto Currency to specified address

        Parameters:
            :remittee_list_id RemitteeList Id sending to
            :amount Amount
            :purpose_type Purpose Type
            :purpose_details Purpose Details

        Returns:
            :remittee_list_id RemitteeList Id sending to
            :amount Amount
            :purpose_details
                :specific_items_of_goods Specific Items of Goods
                :place_of_origin Place of Origin
                :place_of_loading Place of Loading
            ...
        """
        method_name = self.get_method_name()
        payload = {
            "remittee_list_id": remittee_list_id,
            "amount": amount,
            "purpose_type": purpose_type,
            "purpose_details": purpose_details,
        }
        self.log.info(
            method_name, f"Fetching Send Crypto Currency for Parameters {payload}"
        )
        return self.private_request(method_name, **payload)

    def get_send_crypto_history(self, pair):
        """
        Sending History
        BTC Sending history

        Parameters:
            :currency Currency(Only BTC)
        Returns:
            :id Send
            :amount Amount of bitcoins sent
            :fee Fee
            :currency Currency
            :address Recipient's bitcoin address
            :created_at Date you sent
            ...
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Sending History for {pair}")
        return self.private_request(method_name, pair=pair)

    def get_deposits_istory(self, pair):
        """
        Deposits History
        BTC deposit history

        Parameter:
            :currency Currency(BTC now)
        Returns:
            :id Send
            :amount Amount of bitcoins sent
            :currency Currency
            :address Recipient's bitcoin address
            :status Status
            :confirmed_at Date Confirmed
            :created_at Date when receiving process started
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Deposits History for {pair}")
        return self.private_request(method_name, pair=pair)

    def get_account_information(self):
        """
        Account information
        Display account information.

        Returns:
            :id Send
            :email Registered e-mail
            :identity_status Your identity status.
            :bitcoin_address Your bitcoin address for deposit
            :taker_fee It displays the fee rate (%) in the case of performing the order as Taker.(BTC_JPY)
            :maker_fee It displays the fee rate (%) in the case of performing the order as Maker.(BTC_JPY)
            :exchange_fees It displays the fee for each order book.
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Deposits History")
        return self.private_request(method_name)

    # Withdraw JPY
    # You can withdraw JPY through this API.
    def get_bank_account_list(self):
        """
        Bank account list
        Display list of bank account you registered (withdrawal).

        Returns:
            :id Send
            :bank_name Bank name
            :branch_name Branch name
            :bank_account_type Type of bank account
            :number Bank account number
            :mname Bank account name
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Bank account list")
        return self.private_request(method_name)

    def delet_bank_account(self, id):
        """
        Remove bank account
        Will remove your bank account.

        Parameters:
            :id Bank account list iD
        Return:
            :success Removing bank account success
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Remove bank account with id: {id}")
        return self.private_request(method_name, id=id)

    def get_withdraw_history(self):
        """
        Withdraw history
        Display Japanese YEN withdrawal request history.

        Returns:
            :id Send
            :status Withdraw status (pending, processing, finished, canceled)
            :amount Amount
            :currency Currency
            :created_at Date you created
            :bank_account_id Bank account ID
            :fee Fee
            :is_fast Fast withdraw option. Currently stopped.
        """
        method_name = self.get_method_name()
        self.log.info(method_name, f"Fetching Withdraw history")
        return self.private_request(method_name)

    def post_create_withdraw(self, bank_account_id, amount, currency):
        """
        Create withdraw
        Request Japanese Yen withdrawal

        Parameters:
            :bank_account_id Bank account ID
            :amount Amount
            :currency Currency ( only "JPY" )
        Returns:
            :id Send
            :status Withdraw status (pending, processing, finished, canceled)
            :amount Amount
            :currency Currency
            :created_at Date you created
            :bank_account_id Bank account ID
            :fee Fee
        """
        method_name = self.get_method_name()
        payload = {
            "bank_account_id": bank_account_id,
            "amount": amount,
            "currency": currency,
        }
        self.log.info(method_name, f"Fetching Create withdraw for Parameters{payload}")
        return self.private_request(method_name, **payload)
