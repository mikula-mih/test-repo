
# class responsibilities:
# - "passive" classes = hold objects and maintain an internal state;
# - "active" classes = reach out into other objects to take action and so smth;
""" the `Command` pattern """
# the `Command` pattern generally involves a hierarchy of classes that each do
# smth; A Core class can create a command (or a sequence of commands) to carry
# out actions;
# a kind of meta-programming: by creating Command object that contain a bunch
# of statements, the design has a higher-level "language" of Command objects;
import random
#
def dice_roller(request: bytes) -> bytes:
    request_text = request.decode("utf-8")
    numbers = [random.randint(1, 6) for _ in range(6)]
    response = f"{request_text} = {numbers}"
    return response.encode("utf-8")
#
import re
# 1. the first frouping: (?P<n>\d*)
#       captures a batch of digits for the number of dice,
#       saving this as a group named "n"; this's optional, allowing to write
#       d6 insread of 1d6.
# 2. the letter "d", which must be present, but isn't captured;
# 3. the next grouping: (?P<d>\d+)
#       captures the digits for the number of faces on each dice;
#       (4|6|8|10|12|20|100) to define an acceptable list of regular
#       polyhedral dice (and two common irregular polyhedrons);
# 4. the final grouping: (?P<a>[dk+_]\d+)*
#       defines a repeating series of adjustments;
#       each one has a prefix and a sequence of digits: d1, k3, +1, -2;
#       capture the whole sequence as group "a", and decompose the parts
#       separately; each of the parts will become a command;
dice_pattern = re.compile(r"(?P<n>\d*)d(?P<d>\d+)(?P<a>[dk+-]\d+)*")
#
class Dice:
    def __init__(self, n: int, d: int, *adj: Adjustment) -> None:
        self.adjustments = [cast(Adjustment, Roll(n, d))] + list(adj)
        self.dice: list[int]
        self.modifier: int

    def roll(self) -> int:
        for a in self.adjustments:
            a.apply(self)
        return sum(self.dice) + self.modifier

    @classmethod
    def from_text(cls, dice_text: str) -> "Dice":
        dice_pattern = re.compile(
            r"(?P<n>\d*)d(?P<d>\d+)(?P<a>[dk+-]\d+)*")
        adjustment_pattern = re.compile(r"([dk+-])(\d+)")
        adj_class: dict[str, Type[Adjustment]] = {
            "d": Drop,
            "k": Keep,
            "+": Plus,
            "-": Minus,
        }

        if (dice_match := dice_pattern.match(dice_text)) is None:
            raise ValueError(f"Error in {dice_text!r}")

        n = int(dice_match.group("n")) if dice_match.group("n") else 1
        d = int(dice_match.group("d"))
        adjustment_matches = adjustment_pattern.finditer(
            dice_match.group("a") or "")
        adjustment = [
            adj_class[a.group(1)](int(a.group(2)))
            for a in adjustment_matches
        ]
        return cls(n, d, *adjustments)


class Adjustment(abc.ABC):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    @abc.abstractmethod
    def apply(self, dice: "Dice") -> None:
        ...


class Roll(Adjustment):
    def __init__(self, n: int, d: int) -> None:
        self.n = n
        self.d = d

    def apply(self, dice: "Dice") -> None:
        dice.dice = sorted(
            random.randint(1, self.d) for _ in range(self.n))
        dice.modifier = 0


class Drop(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.dice = dice.dice[self.amount :]


class Keep(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.dice = dice.dice[: self.amount]


class Plus(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.modifier += self.amount


class Minus(Adjustment):
    def apply(self, dice: "Dice") -> None:
        dice.modifier -= self.amount

#
