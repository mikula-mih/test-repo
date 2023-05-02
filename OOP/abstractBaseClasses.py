from __future__ import annotations
# `Duck typing`: When two class definitions have the same attributes and
# methods, then instances of the two classes have the same protocol and can
# be used interchangeably.
# `Inheritance`: When two class definitions have common aspects, a subclass
# can share common features of a superclass. The implementation details of
# the two classes may vary, but the classes should be interchangeable when
# we use the common features defined by the superclass.

""" Abstract Base Classes & Operator Overloading """
import abc
# define the media player as an `abstraction`; Each unique kind of media file
# format can provide a concrete implementation of the abstraction;
class MediaLoader(abc.ABC):
    # the `abc.ABC` class introduces a `metaclass`:
    # a class used to build the concrete class definitions
    # Python's default metaclass is named `type`
    @abc.abstractmethod
    def play(self) -> None:
        # three-dot token, the ellipsis
        ...
# the Python code to remind everyone a useful body needs to be written
# in order to create a working, concrete subclass;
    @property
    @abc.abstractmethod
    def ext(self) -> str:
        ...
# the consequences of marking these properties is the class now has a new
# special attribute, `__abstractmethods__`; it lists all of the names that need
# to be filled in to create a concrete class;
print(MediaLoader.__abstractmethods__)
class Ogg(MediaLoader):
    ext = '.ogg'
    def play(self):
        pass
o = Ogg()

""" the ABCs of collections """
# the `collections` module: defines the built-in generic collections using
# a sophisticated set of base classes and mixins;
from collections.abc import Container
print(Container.__abstractmethods__)
help(Container.__contains__)

class OddIntegers:
    def __contains__(self, x: int) -> bool:
        return x % 2 != 0

odd = OddIntegers()
print(1 in odd, 2 in odd, 3 in odd)

""" Abstract base classes and type hints """
# the concept of `parameterizing the generic type` to make if more specific
# often applies to abstract classes;
# the `protocol`; essence of how duck typing works: when two classes have the
# same batch of methods, they both adhere to a common protocol;
x = dict({"a": 42, "b": 7, "c": 6})
# def __init__(self, source: BaseMapping) -> None
y = dict([("a", 42), ("b", 7), ("c", 6)])
# def __init__(self, source: Iterable[tuple[Comparable, Any]]) -> None
print(x == y)
# provide `overloaded` method definitions;
# done with a special decoration from the `typing` module, `@overload`;
from collections import abc
from typing import Protocol, Any, overload, Union
import bisect
from typing import Iterator, Iterable, Sequence, Mapping

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __lt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...

BaseMapping = abc.Mapping[Comparable, Any]
class Lookup(BaseMapping):
    @overload
    def __init__(
        self,
        source: Iterable[tuple[Comparable, Any]]
    ) -> None:
        ...

    @overload
    def __init__(self, source: BaseMapping) -> None:
        ...

    def __init__(
        self,
        source: Union[Iterable[
        tuple[Comparable, Any]],
        BaseMapping,
        None] = None,
    ) -> None:
        sorted_pairs: Sequence[tuple[Comparable, Any]]
        if isinstance(source, Sequence):
            sorted_pairs = sorted(source)
        elif isinstance(source, abc.Mapping):
            sorted_pairs = sorted(source.items())
        else:
            sorted_pairs = []
        self.key_list = [p[0] for p in sorted_pairs]
        self.value_list = [p[1] for p in sorted_pairs]

    def __len__(self) -> int:
        return len(self.key_list)

    def __iter__(self) -> Iterator[Comparable]:
        return iter(self.key_list)

    def __contains__(self, key: object) -> bool:
        index = bisect.bisect_left(self.key_list, key)
        return key == self.key_list[index]

    def __getitem__(self, key: Comparable) -> Any:
        index = bisect.bisect_left(self.key_list, key)
        if key == self.key_list[index]:
            return self.value_list[index]
        raise KeyError(key)


x = Lookup(
    [
        ["z", "Zillah"],
        ["a", "Amy"],
        ["c", "Clara"],
        ["b", "Basil"],
    ]
)
try:
    print(x["c"])
    x["m"] = "Maud"
except TypeError as er:
    print(f"Caught an  error: {er!r}")

""" create `abstract base class` """
import abc
import random

class Die(abc.ABC):
    def __init__(self) -> None:
        self.face: int
        self.roll()

    @abc.abstractmethod
    def roll(self) -> None:
        ...

    def __repr__(self) -> str:
        return f"{self.face}"

class D6(Die):
    def roll(self) -> None:
        self.face = random.randint(1, 6)

class Dice(abc.ABC):
    def __init__(self, n: int, die_class: Type[Die]) -> None:
        self.dice = [die_class() for _ in range(n)]

    @abc.abstractmethod
    def roll(self) -> None:
        ...

    @property
    def total(self) -> int:
        return sum(d.face for d in self.dice)

class SimpleDice(Dice):
    def roll(self) -> None:
        for d in self.dice:
            d.roll()

class YachtDice(Dice):
    def __init__(self) -> None:
        super().__init__(5, D6)
        self.saved: Set[int] = set()

    def saving(self, positions: Iterable[int]) -> "YachtDice":
        if not all(0 <= 6 for n in positions):
            raise ValueError("Invalid position")
        self.saved = set(positions)
        return self

    def roll(self) -> None:
        for n, d in enumerate(self.dice):
            if n not in self.saved:
                d.roll()
        self.saved = set()

sd = YachtDice()
sd.roll()
print(sd.dice)
sd.saving([0, 1, 2]).roll()
print(sd.dice)
# the `type` object is called the `metaclass`, the class used to build classes;
# every class object is an instance of `type`;
class DieM(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.face: int
        self.roll()

    @abc.abstractmethod
    def roll(self) -> None:
        ...
# a class `abc.ABCMeta` extends the `type` class to check for methods decorated
# with `@abstractmethod`; the special `__mro__` attribute of the ABCMeta metaclass;
# this attribute lists the classes used for resolving method names(MRO:
# Method Resolution Order);

""" Operator oveloading """
# Python's operators, +, /, -, *, and so on, are implemented by special
# methods on classes.
# the `__len__()` method is used by the built-in len() function
# the `__iter__()`` method is used by the built-in iter() function, which means
# it's used by the for statement
# the `__contains__()`` method is used by the built-in in operator
class DDice:
    def __init__(self, *die_class: Type[Die]) -> None:
        self.dice = [dc() for dc in die_class]
        self.adjust: int = 0

    def plus(self, adjust: int = 0) -> "DDice":
        self.adjust = adjust
        return self

    def roll(self) -> None:
        for d in self.dice:
            d.roll()

    @property
    def total(self) -> int:
        return sum(d.face for d in self.dice) + self.adjust
# the `/` operator is implemented by the `__truediv__()` and `__rtruediv__()` methods
    def __add__(self, die_class: Any) -> "DDice":
        if isinstance(die_class, type) and issubclass(die_class, Die):
            new_classes = [type(d) for d in self.dice] + [die_class]
            new = DDice(*new_classes).plus(self.adjust)
            return new
        elif isinstance(die_class, int):
            new_classes = [type(d) for d in self.dice]
            new = DDice(*new_classes).plus(die_class)
            return new
        else:
            return NotImplemented

    def __radd__(self, die_class: Any) -> "DDice":
        if isinstance(die_class, type) and issubclass(die_class, Die):
            new_classes = [die_class] + [type(d) for d in self.dice]
            new = DDice(*new_classes).plus(self.adjust)
            return new
        elif isinstance(die_class, int):
            new_classes = [type(d) for d in self.dice]
            new = DDice(*new_classes).plus(die_class)
            return new
        else:
            return NotImplemented
# `__iadd__()` and `__imul__()` are "in-place" operations, designed to mutate object
    def __mul__(self, n: Any) -> "DDice":
        if isinstance(n, int):
            new_classes = [type(d) for d in self.dice for _ in range(n)]
            return DDice(*new_classes).plus(self.adjust)
        else:
            return NotImplemented

    def __rmul__(self, n: Any) -> "DDice":
        if isinstance(n, int):
            new_classes = [type(d) for d in self.dice for _ in range(n)]
            return DDice(*new_classes).plus(self.adjust)
        else:
            return NotImplemented

    def __iadd__(self, die_class: Any) -> "DDice":
        if isinstance(die_class, type) and issubclass(die_class, Die):
            self.dice += [die_class()]
            return self
        elif isinstance(die_class, int):
            self.adjust += die_class
            return self
        else:
            return NotImplemented

""" Extending built-ins """
# Python has two collections of built-ins that we might want to extend, that can
# be broadly classified into the following:
# 1. Immutable objects, including numbers, strings, bytes, and tuples;
# 2. Mutable collections, including sets, lists, and dictionaries;
from typing import Dict, Hashable, Any, Mapping, Iterable
from typing import cast, Union, Tuple
# from collections import Hashable

DictInit = Union[
    Iterable[Tuple[Hashable, Any]],
    Mapping[Hashable, Any],
    None]

class NoDupDict(Dict[Hashable, Any]):
    def __setitem__(self, key: Hashable, value: Any) -> None:
        if key in self:
            raise ValueError(f"duplicate {key!r}")
        super().__setitem__(key, value)

    def __init__(self, init: DictInit = None, **kwargs: Any) -> None:
        if isinstance(init, Mapping):
            super().__init__(init, **kwargs)
        elif isinstance(init, Iterable):
            for k, v in cast(Iterable[Tuple[Hashable, Any]], int):
                self[k] = v
        elif init is None:
            super().__init__(**kwargs)
        else:
            suepr().__init__(init, **kwargs)
# in the case of sequence of key-value pairs, we can use the previously defined
# `__setitem__()` to raise an exception in the event of duplicate key values;
# implement `update()`, `setdefault()`, `__or__()`, and `__ior__()` to extend
# all the methods that can mutate a dictionay;
nd = NoDupDict()
# studing `collections.abc`, we need to extend a mapping, with a changed
# definition of `__setitem__()` to prevent updating an existing key;

""" Metaclasses """
# the job of the `type` class is to create an empty class object so the various
# definitions and attributes assignment statements will build the final, usable
# class we need for our application;
#
# the `class` statement is used to locate the appropriate metaclass;
# if no special `metaclass=` is provided, then the `type` class is used;
# the `type` class will prepare a new, empty dictionary, called a namespace, and
# then the various statements in the class populate this container with
# attributes and method definitions;
import logging
from functools import wraps
from typing import Type, Any

class DieMeta(abc.ABCMeta):
    def __new__(
        metaclass: Type[type],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> "DieMeta":
        if "roll" in namespace and not getattr(
            namespace["roll"], "__isabatractmethod__", False
        ):
            namespace.setdefault("logger", logging.getLogger(name))

            original_method = namespace["roll"]

            @wraps(original_method)
            def logged_roll(self: "DieLog") -> None:
                original_method(self)
                self.logger.info(f"Rolled {self.face}")

            namespace["roll"] = logged_roll
        new_object = cast(
            "DieMeta", abc.ABCMeta.__new__(
                metaclass, name, bases, namespace)
        )
        return new_object


class DieLong(metaclass=DieMeta):
    logger: logging.Logger

    def __init__(self) -> None:
        self.face: int
        self.roll()

    @abc.abstractmethod
    def roll(self) -> None:
        ...

    def __repr__(self) -> str:
        return f"{self.face}"


class D6L(DieLong):
    def roll(self) -> None:
        """Some documentation on D6L"""
        self.face = random.randrange(1, 7)
#
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
d2 = D6L()
print(d2.face)
