# broker_config.py
class BrokerConfig:
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


# Define instances for broker1 and broker2
coincheck = BrokerConfig(
    access_key="",
    secret_access_key="",
    base_url="https://coincheck.com",
    api_urls={
        "get_ticker": "/api/ticker",
        "get_trades": "/api/trades",
        "get_orderbooks": "/api/order_books",
        "get_calc_rate": "/api/exchange/orders/rate",
        "get_standard_rate": "/api/rate/{}",  # /api/rate/[pair]
        "get_accounts": "/api/accounts",
        "get_accounts_ticker": "/api/accounts/ticker",
        "get_accounts_balance": "/api/accounts/balance",
        "post_new_order": "/api/exchange/orders",
        "get_unsettled_order_list": "/api/exchange/orders/opens",
        "delet_cancel_order": "/api/exchange/orders/{}",  # /api/exchange/orders/[id]
        "get_order_cancellation_status": "/api/exchange/orders/cancel_status",  # /api/exchange/orders/cancel_status?id=[id]
        "exchange_orders_transactions": "/api/exchange/orders/transactions",
        "exchange_orders_transactions_pagination": "/api/exchange/orders/transactions_pagination",
        "send_money": "/api/send_money",
        "deposit_money": "/api/deposit_money",
        "bank_accounts": "/api/bank_accounts",
        "remove_bank_account": "/api/bank_accounts/",  # /api/bank_accounts/[id]
        "withdraws": "/api/withdraws",
        "cancel_withdrawal_request": "/api/withdraws/",  # /api/withdraws/[id]
    },
)
broker1_config = BrokerConfig(
    access_key="your_broker2_api_key",
    secret_access_key="your_broker2_secret_key",
    account_id="your_broker2_account_id",
    base_url="",
)
