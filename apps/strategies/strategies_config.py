from dataclasses import dataclass


@dataclass
class StrategiesConfig:
    moving_average_window: int = 20
    std_dev_multiplier: int = 2
    rsi_period: int = 14