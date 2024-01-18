# UniversalTraderX (UTX)

UniversalTraderX (UTX) is a versatile and broker-agnostic trading bot designed to interact with brokers across various asset classes, including gold, FX (Forex), cryptocurrencies, and more. UTX provides a flexible and modular architecture for trading, backtesting, and generating strategies for different financial products.

## Overview

- **Broker Agnosticism:** UTX is designed to be broker-agnostic, allowing it to seamlessly interact with various brokers across different asset classes and financial products.

- **Strategy Generation and Backtesting:** The system includes modules for generating and backtesting trading strategies. Users can implement custom strategies or choose from predefined ones.

- **Data Handling and Manipulation:** UTX incorporates efficient data handling and manipulation tools to ensure the reliability and accuracy of trading decisions.

- **Versatile Configuration:** Configuration files in the `config/` directory allow users to tailor the system to their preferred brokers, asset classes, and specific trading strategies.

# Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/UniversalTraderX.git
   
## 1. Install dependencies:
cd UniversalTraderX
pip install -r requirements.txt

## 2. Configure API and broker settings in the config/ directory.

## 3. Run the trading bot:
./torun.sh

# Docker
### Build the Docker image:
    docker build -t utx .

### Run the Docker container:
    docker run -it --rm utx

### Docker Compose
A Docker Compose file is provided in the docker/ directory to simplify the setup.
## Adjust the configurations as needed.
    cd utx/docker
    docker-compose up

# Strategy Generation and Backtesting
UTX supports the generation and backtesting of trading strategies.
The strategies/ directory contains predefined strategies (e.g., strategy1.py, strategy2.py).
Users can implement custom strategies based on their preferences.
To backtest a strategy, run the following command:
    jesse backtest --strategy YourStrategyName

# Customization
### Strategy Implementation:
Users can implement custom trading strategies by creating new modules in the strategies/ directory.

### Configuration:
Adjust the configuration settings in the config/ directory to match your preferred brokers, asset classes, and trading strategies.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
