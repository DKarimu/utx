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
        "ticker": "/api/ticker",
        "trades": "/api/trades",
        "order_books": "/api/order_books",
    },
)
broker1_config = BrokerConfig(
    base_url="",
    api_key="your_broker2_api_key",
    secret_key="your_broker2_secret_key",
    account_id="your_broker2_account_id",
    base_url="",
)
