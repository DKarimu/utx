class BrokersConfig:
    def __init__(
        self,
        access_key=None,
        secret_access_key=None,
        account_id=None,
        base_url=None,
        api_urls=None,
        **kwargs
    ):
        self.api_key = access_key
        self.secret_key = secret_access_key
        self.account_id = account_id
        self.base_url = base_url
        self.api_urls = api_urls
        self.additional_params = kwargs


# Define instances for coincheck
coincheck_cfg = BrokersConfig(
    access_key="",
    secret_access_key="",
    base_url="https://coincheck.com",
    api_urls={
        # Public API
        "get_ticker": "/api/ticker",
        "get_public_trades": "/api/trades",
        "get_orderbooks": "/api/order_books",
        "get_calc_rate": "/api/exchange/orders/rate",
        "get_standard_rate": "/api/rate/{}",
        "get_accounts": "/api/accounts",
        "get_accounts_ticker": "/api/accounts/ticker",
        "get_accounts_balance": "/api/accounts/balance",
        # Private API
        "post_new_order": "/api/exchange/orders",
        "get_unsettled_order_list": "/api/exchange/orders/opens",
        "delet_cancel_order": "/api/exchange/orders/{}",
        "get_order_cancellation_status": "/api/exchange/orders/cancel_status",
        "get_transaction_history": "/api/exchange/orders/transactions",
        "get_transaction_history_pagination": "/api/exchange/orders/transactions_pagination",
        # Balance
        "get_balance": "/api/accounts/balance",
        "get_send_crypto_currency": "/api/send_money",
        "get_send_crypto_history": "/api/send_money",
        "get_deposits_istory": "/api/deposit_money",
        "get_account_information": "/api/accounts",
        "get_bank_account_list": "/api/bank_accounts",
        "delet_bank_account": "/api/bank_accounts/{}",
        "get_withdraw_history": "/api/withdraws",
        "post_create_withdraw": "/api/withdraws",
    },
)

broker1_config = BrokersConfig(
    access_key="your_broker2_api_key",
    secret_access_key="your_broker2_secret_key",
    account_id="your_broker2_account_id",
    base_url="",
)
