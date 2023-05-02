
""" The Strategy Pattern """
# you can swap out algorithms without changing the code that uses the algorithm;
# use strategy pattern to switch between different file compression algorithms;

import statistics
from abc import ABC, abstractmethod

class ExchangeConnectionError(Exception):
    """Custom error that is raised when an exchange is not connected."""


class Exchange:
    """Basic exchange simulator."""

    def __init__(self) -> None:
        self.connected = False

    def connect(self) -> None:
        """Connect to the exchange."""
        print("Connecting to Crypto exchange...")
        self.connected = True

    def check_connection(self) -> None:
        """Check if the exchange is connected."""
        if not self.connected:
            raise ExchangeConnectionError()

    def get_market_data(self, symbol: str) -> list[float]:
        """Return fake market price data for a given market symbol."""
        self.check_connection()

        price_data = {
            "BTC/USD": [
                35842.0,
                34069.0,
                33871.0,
                34209.0,
                32917.0,
                33931.0,
                33370.0,
                34445.0,
                32901.0,
                33013.0,
            ],
            "ETH/USD": [
                2381.0,
                2233.0,
                2300.0,
                2342.0,
                2137.0,
                2156.0,
                2103.0,
                2165.0,
                2028.0,
                2004.0,
            ],
        }
        return price_data[symbol]

    def buy(self, symbol: str, amount: float) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: float) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Selling amount {amount} in market {symbol}.")


class TradingStrategy(ABC):
    """Trading strategy that decides whether to buy or sell, given a list of prices."""

    @abstractmethod
    def should_buy(self, prices: list[float]) -> bool:
        """Whether you should buy this coin, given the prices."""

    @abstractmethod
    def should_sell(self, prices: list[float]) -> bool:
        """Whether you should sell this coin, given the prices."""


class AverageTradingStrategy(TradingStrategy):
    """Trading strategy based on price averages."""

    def should_buy(self, prices: list[float]) -> bool:
        list_window = prices[-3:]
        return prices[-1] < statistics.mean(list_window)

    def should_sell(self, prices: list[float]) -> bool:
        list_window = prices[-3:]
        return prices[-1] > statistics.mean(list_window)


class MinMaxTradingStrategy(TradingStrategy):
    """Trading strategy based on price minima and maxima."""

    def should_buy(self, prices: list[float]) -> bool:
        # buy if it's below $32,000
        return prices[-1] < 32000

    def should_sell(self, prices: list[float]) -> bool:
        # sell if it's above $33,000
        return prices[-1] > 33000


class TradingBot:
    """Trading bot that connects to a crypto exchange and performs trades."""

    def __init__(self, exchange: Exchange, trading_strategy: TradingStrategy) -> None:
        self.exchange = exchange
        self.trading_strategy = trading_strategy

    def run(self, symbol: str) -> None:
        """Run the trading bot once for a particular symbol, with a given strategy."""
        prices = self.exchange.get_market_data(symbol)
        should_buy = self.trading_strategy.should_buy(prices)
        should_sell = self.trading_strategy.should_sell(prices)
        if should_buy:
            self.exchange.buy(symbol, 10)
        elif should_sell:
            self.exchange.sell(symbol, 10)
        else:
            print(f"No action needed for {symbol}.")


def main() -> None:
    """
    Create an exchange and a trading bot with a strategy.
    Run the strategy once on a particular symbol.
    """

    # create the exchange and connect to it
    exchange = Exchange()
    exchange.connect()

    # create the trading strategy
    trading_strategy = MinMaxTradingStrategy()

    # create the trading bot and run the bot once
    bot = TradingBot(exchange, trading_strategy)
    bot.run("BTC/USD")



if __name__ == "__main__":
    main()
