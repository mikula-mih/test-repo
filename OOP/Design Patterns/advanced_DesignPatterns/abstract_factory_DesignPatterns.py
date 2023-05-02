
# the `Abstract Factory` pattern is appropriate when we have multiple possible
# implementations of a system that depend on some configuration or platform
# detail;
""" the `Abstract Factory` pattern """
# the underlying implementation returned may depend on a variety of factors,
# such as the current locale, operating system, or local configuration;
from enum import Enum, auto
from typing import NamedTuple, List

class Suit(str, Enum):
    Clubs = "\N{Black Club Suit}"
    Diamonds = "\N{Black Diamonds Suit}"
    Hearts = "\N{Black Heart Suit}"
    Spades = "\N{Black Spade Suit}"

class Card(NamedTuple):
    rank: int
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

class Trick(int, Enum):
    pass

class Hand(List[Card]):
    def __init__(self, *cards: Card) -> None:
        super().__init__(cards)

    def scoring(self) -> List[Trick]:
        pass

import abc

class CardGameFactory(abc.ABC):
    @abc.abstractmethod
    def make_card(self, rank: int, suit: Suit) -> "Card":
        ...

    @abc.abstractmethod
    def make_hand(self, *cards: Card) -> "Hand":
        ...

class CribbageCard(Card):
    @property
    def points(self) -> int:
        return self.rank

class CribbageAce(Card):
    @property
    def points(self) -> int:
        return 1

class CribbageFace(Card):
    @property
    def points(self) -> int:
        return 10

class CribbageHand(Hand):
    starter: Card

    def upcard(self, starter: Card) -> "Hand":
        self.starter = starter
        return self

    def scoring(self) -> list[Trick]:
        """15's. Pairs. Runs. Right Jack."""
        # ... details omitted ...
        return tricks

class PokerCard(Card):
    def __str__(self) -> str:
        if self.rank == 14:
            return f"A{self.suit}"
        return f"{self.rank}{self.suit}"

class PokerHand(Hand):
    def scoring(self) -> list[Trick]:
        """Return a single 'Trick'"""
        # ... details omitted ...
        return [rank]

class PokerFactory(CardGameFactory):
    def make_card(self, rank: int, suit: Suit) -> "Card":
        if rank == 1:
            # Aces above kings
            rank = 14
        return PokerCard(rank, suit)

    def make_hand(self, *cards: Card) -> "Hand":
        return PokerHand(*cards)
#
factory = CribbageFactory()
cards = [
    factory.make_card(6, Suit.Clubs),
    factory.make_card(7, Suit.Diamonds),
    factory.make_card(8, Suit.Hearts),
    factory.make_card(9, Suit.Spades),
]
starter = factory.make_card(5, Suit.Spades)
hand = factory.make_hand(*cards)
score = sorted(hand.upcard(starter).scoring())
print(
    list(t.name for t in score)
)
#
class CardGameFactoryProtocol(Protocol):
    def make_card(self, rank: int, suit: Suit) -> "Card":
        ...

    def make_hand(self, *cards: Card) -> "Hand":
        ...
#
