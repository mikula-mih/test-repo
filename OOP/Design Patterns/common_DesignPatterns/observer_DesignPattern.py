from __future__ import annotations
# the `Observer` pattern is usefull for state monitoring and event handling
# situations; this pattern allows a given object to be monitored by an unknown
# and dynamic group of `observer` objects; the core object being observed
# needs to implement an interface that makes it observable;
""" the `Observer` pattern """
# In Python, the observer can be notified via the `__call__()` method, making
# each observer behave like a function or other callable object;
from typing import Protocol, List

class Observer(Protocol):
    def __call__(self) -> None:
        ...


class Observable:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def _notify_observers(self) -> None:
        for observer in self._observers:
            observer()

Hand = List[int]

class ZonkHandHistory(Observable):
    def __init__(self, player: str, dice_set: Dice) -> None:
        super().__init__()
        self.player = player
        self.dice_set = dice_set
        self.rolls: list[Hand]

    def start(self) -> Hand:
        self.dice_set.roll()
        self.rolls = [self.dice_set.dice]
        self._notify_observers()    # State change
        return self.dice_set.dice

    def roll(self) -> Hand:
        self.dice_set.roll()
        self.rolls.append(self.dice_set.dice)
        self._notify_observers()    # State change
        return self.dice_set.dice


class SaveZonkHand(Observer):
    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.count = 0

    def __call__(self) -> None:
        self.count += 1
        message = {
            "player": self.hand.player,
            "sequence": self.count,
            "hands": json.dumps(self.hand.rolls),
            "time": time.time(),
        }
        print(f"SaveZonkHand {message}")
#
d = Dice.from_text("6d6")
player = ZonkHandHistory("Bo", d)

save_history = SaveZonkHand(player)
player.attach(save_history)
r1 = player.start()

r2 = player.roll()
#
class ThreePairZonkHand:
    """Observer of ZonkHandHistory"""
    def __init__(self, hand: ZonkHandHistory) -> None:
        self.hand = hand
        self.zonked = False

    def __call__(self) -> None:
        last_roll = self.hand.rolls[-1]
        distinct_values =set(last_roll)
        self.zonked = len(distinct_values) == 3 and all(
            last_roll.count(v) == 2 for v in distinct_values
        )
        if self.zonked:
             print("3 Pair Zonk!")
#
