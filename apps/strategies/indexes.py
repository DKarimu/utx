class Indexes:

    def calculate_bollinger_bands(
        self, rates, moving_average_window, std_dev_multiplier
    ):
        rolling_mean = rates.rolling(window=moving_average_window).mean()
        rolling_std = rates.rolling(window=moving_average_window).std()
        upper_band = rolling_mean + (rolling_std * std_dev_multiplier)
        lower_band = rolling_mean - (rolling_std * std_dev_multiplier)
        return rolling_mean, upper_band, lower_band

    pass

    def calculate_rsi(self, rates, rsi_period):
        delta = rates.diff().dropna()
        gain = delta.where(delta > 0, 0).rolling(window=rsi_period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        normalized_rsi = (rsi - 50) * 0.02
        return normalized_rsi

    def calculate_price_volatility(self, rates):
        volatility = rates.std()
        return volatility
