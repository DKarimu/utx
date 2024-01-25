# broker_config.py
class BrokerConfig:
    def __init__(
        self,
        api_key=None,
        secret_key=None,
        account_id=None,
        base_url=None,
        api_urls=None,
        **kwargs
    ):
        self.api_key = api_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.base_url = base_url
        self.api_urls = api_urls
        self.additional_params = kwargs


# Define instances for broker1 and broker2
coincheck = BrokerConfig(
    api_key="coincheck_api_key",
    secret_key="coincheck_secret_key",
    base_url="https://coincheck.com",
    api_urls={
        "accounts": "/api/accounts",
        "accounts_ticker": "/api/accounts/ticker",
        "accounts_balance": "/api/accounts/balance",
        "ticker": "/api/ticker",
        "trades": "/api/trades",
        "order_books": "/api/order_books",
        "exchange_orders_rate": "/api/exchange/orders/rate",
        "rate_pair": "/api/rate/",  # /api/rate/[pair]
        "exchange_orders": "/api/exchange/orders",
        "exchange_orders_opens": "/api/exchange/orders/opens",
        "exchange_orders_id": "/api/exchange/orders/",  # /api/exchange/orders/[id]
        "exchange_orders_cancel_status": "/api/exchange/orders/cancel_status?id=",  # /api/exchange/orders/cancel_status?id=[id]
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
    api_key="your_broker2_api_key",
    secret_key="your_broker2_secret_key",
    account_id="your_broker2_account_id",
    base_url="",
)
