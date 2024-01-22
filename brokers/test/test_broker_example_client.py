# test_broker_example_client.py
from django.test import TestCase
from brokers.config.broker_config import *


class ApiSettingsTest(TestCase):
    def test_broker1_config(self):
        # Creating an instance of BrokerConfig for broker1
        config = BrokerConfig(
            api_key="your_broker1_api_key",
            secret_key="your_broker1_secret_key",
            account_id="your_broker1_account_id",
            # Add any other specific configuration parameters for broker1
        )

        self.assertEqual(broker1_config.api_key, config.api_key)
        self.assertEqual(broker1_config.secret_key, config.secret_key)
        self.assertEqual(broker1_config.account_id, config.account_id)
        # Add any additional assertions for broker1_config

    def test_broker2_config(self):
        # Creating an instance of BrokerConfig for broker2
        config = BrokerConfig(
            api_key="your_broker2_api_key",
            secret_key="your_broker2_secret_key",
            account_id="your_broker2_account_id",
            # Add any other specific configuration parameters for broker2
        )

        self.assertEqual(broker1_config.api_key, config.api_key)
        self.assertEqual(broker1_config.secret_key, config.secret_key)
        self.assertEqual(broker1_config.account_id, config.account_id)
        # Add any additional assertions for broker2_config
