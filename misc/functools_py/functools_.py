import statistics
from dataclasses import dataclass
from typing import Protocol


PRICE_DATA = {
    "BTC/USD": [
        35_842_00,
        34_069_00,
        33_871_00,
        34_209_00,
        32_917_00,
        33_931_00,
        33_370_00,
        34_445_00,
        32_901_00,
        33_013_00,
    ],
    "ETH/USD": [
        2_381_00,
        2_233_00,
        2_300_00,
        2_342_00,
        2_137_00,
        2_156_00,
        2_103_00,
        2_165_00,
        2_028_00,
        2_004_00,
    ],
}


class ExchangeConnectionError(Exception):
    """Custom error that is raised when an exchange is not connected."""


class Exchange:
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

    def get_market_data(self, symbol: str) -> list[int]:
        """Return fake market price data for a given market symbol."""
        self.check_connection()
        return PRICE_DATA[symbol]

    def buy(self, symbol: str, amount: int) -> None:
        """Simulate buying an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Buying amount {amount} in market {symbol}.")

    def sell(self, symbol: str, amount: int) -> None:
        """Simulate selling an amount of a given symbol at the current price."""
        self.check_connection()
        print(f"Selling amount {amount} in market {symbol}.")


"""
Basic example of a Trading bot with a strategy pattern.
"""

class TradingStrategy(Protocol):
    """Trading strategy that decides whether to buy or sell, given a list of prices."""

    def should_buy(self, prices: list[int]) -> bool:
        raise NotImplementedError()

    def should_sell(self, prices: list[int]) -> bool:
        raise NotImplementedError()


class AverageTradingStrategy:
    """Trading strategy based on price averages."""

    def should_buy(self, prices: list[int]) -> bool:
        list_window = prices[-3:]
        return prices[-1] < statistics.mean(list_window)

    def should_sell(self, prices: list[int]) -> bool:
        list_window = prices[-3:]
        return prices[-1] > statistics.mean(list_window)


class MinMaxTradingStrategy:
    """Trading strategy based on price minima and maxima."""

    def should_buy(self, prices: list[int]) -> bool:
        # buy if it's below $32,000
        return prices[-1] < 32_000_00

    def should_sell(self, prices: list[int]) -> bool:
        # sell if it's above $33,000
        return prices[-1] > 33_000_00


@dataclass
class TradingBot:
    """Trading bot that connects to a crypto exchange and performs trades."""

    exchange: Exchange
    trading_strategy: TradingStrategy

    def run(self, symbol: str) -> None:
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
