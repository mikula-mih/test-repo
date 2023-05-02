from __future__ import annotations


""" Empty Objects """
o = object()
# o.x = "hello" # has no attribute

""" Tuples """
# `Tuples` are objects that can store a specific number of other objects
# in sequence, they are immutable
import datetime
def middle(stock, date):    # `tuple unpacking`
    symbol, current, high, low = stock
    return (((high + low) / 2), date)

a = 42,     # >>>(42,)
# when Python displays a tuple, it uses the `canonical` representation;
# trailing commas in Python are politely ignored;

""" Named tuples via typing.NamedTuple """
# Named tuples are a great way to create an immutable grouping of data values.
from typing import NamedTuple
class Stock(NamedTuple):
    symbol: str
    current: float
    high: float
    low: float
    @property
    def middle(self) -> float:
        return (self.high + self.low)/2

s = Stock("AAPL", 123.00, 137.99, 53.33)
s2 = Stock("AAPL", 123.00, high=137.99, low=53.33)
symbol, current, high, low = s
print(s.high, s[2], high, s.middle)
# The tuple can contain mutable elements.
t = ("str", ["str", "str"])
t[1].append("another_str")
# tuple t contains a mutable list, therefore it doesn't have a hash value

""" Dataclasses """
from dataclasses import dataclass
@dataclass
class Stock:
    symbol: str
    # you can specify a default value for the attributes of a dataclass
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0
# for this case, the definition is nearly identical to the NamedTuple definition
# the dataclass function is applied as a class decorator, using the `@` operator
s = Stock("AAPL", 123.00, 137.99, 53.33)
s.current = 122.5   # can update attributes
s.unexpected_attribute = 'allowed'
# The `order=True` parameter to the decorator leads to the creation of all of
# the comparison special methods
@dataclass(order=True)
class StockOrdered:
    name: str
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0

stock_ordered1 = StockOrdered("GOOG", 1826.77, 1847.20, 1013.54)
stock_ordered2 = StockOrdered("GOOG")
stock_ordered3 = StockOrdered("GOOG", 1728.28, high=1733.18, low=1666.33)
print(stock_ordered1 < stock_ordered2,
      stock_ordered1 > stock_ordered2)
from pprint import pprint
pprint(sorted([stock_ordered1, stock_ordered2, stock_ordered3]))
# `frozen=True` creates a class that's similar to a typing.NamedTuple

""" Dictionaries """
def letter_frequency(sentence: str) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0)
        frequencies[letter] = frequency + 1
    return frequencies

# `defaultdict` handles missing keys, like `.setdefault`
from collections import defaultdict

def letter_frequency_2(sentence: str) -> defaultdict[str, int]:
    frequencies: defaultdict[str, int] = defaultdict(int)
    for letter in sentence:
        frequencies[letter] = frequency + 1
    return frequencies
#
from dataclasses import dataclass
@dataclass
class Prices:
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0

portfolio = defaultdict(Prices)
print(portfolio["GOOG"])    # >>> Prices(current=0.0, high=0.0, low=0.0)
portfolio["AAPL"] = Prices(current=122.25, high=137.98, low=53.15)
pprint(portfolio)

def make_defaultdict():
    return defaultdict(Prices)

by_month = defaultdict(
    lambda: defaultdict(Prices)
)
by_month["APPL"]["Jan"] = Prices(current=122.25, high=137.98, low=53.15)
pprint(by_month)
#
from collections import Counter
#The `Counter object` behaves like a beefed-up dictionary where the keys are
# the items being counted and the values are the quantities of such items.
def letter_frequency_3(sentence: str) -> Counter[str]:
    return Counter(sentence)
# the `most_common() method` returns a list of (key,count) tuples in descending
# order by the count. You can optionally pass an integer argument into
# most_common() to request a list of only the most common elements
import collections
responses = ["vanilla", "chocolate", "vanilla", "vanilla", "caramel",
    "strawberry", "vanilla"]
favorites = collections.Counter(responses).most_common(1)
name, frequency = favorites[0]
print(name)

""" Lists """
# Don't use lists for collecting different attributes of individual items.
# Tuples, named tuples, dictionaries, and objects are more suitable for that.
import string
CHARACTERS = list(string.ascii_letters) + [" "]
def letter_frequency(sentence: str) -> list[tuple[str, int]]:
    frequencies = [(c, 0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    non_zero = [
        (letter, count)
        for letter, count in frequencies if count > 0
    ]
    return non_zero

""" Sorting lists """
# `sort()` method; for list[str] object will place the items in alphabetical
# order; this operation is case sensitive(all capital letters will be sorted
# before lowercase letters; Z comes before a); for list[num] numerical order;
# for list of tuples, sorted by considering the elements in the tuple in order;
# for mixture containing unsortable items will raise a TypeError exception;
from typing import Optional, cast, Any
from dataclasses import dataclass
import datetime
# the @dataclass(order=True) decorator will assure that all of the comparison
# methods are built for us. A named tuple also has the ordering operations
# defined by default.
@dataclass(frozen=True)
class MultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str
# the special `__lt__()` method(less then) must be defined on the class to make
# instances of that class comparable; method should return True if our class is
# somehow less then the passed parameter, and False otherwise;
    def __lt__(self, other: Any) -> bool:
        if self.data_source == "Local":
            self_datetime = datetime.datetime.fromtimestamp(
                cast(float, self.timestamp)
            )
        else:
            self_datetime = datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            )
        if other.data_source == "Local":
            other_datetime = datetime.datetime.fromtimestamp(
                cast(float, other.timestamp)
            )
        else:
            other_datetime = datetime.datetime.fromisoformat(
                cast(str, other.creation_date)
            )
        return self_datetime < other_datetime
# `tagged union`; a union is a description of an object where attributes are not
# always relevant; if an attribute's relevance depends on another attribute's
# value, this can be seen as a union of distinct subtypes with a tag to
# distinguish between the two types.
mi_0 = MultiItem("Local", 1607280522.68012, None, "Some File", "etc. 0")
mi_1 = MultiItem("Remote", None, "2020-12-06T13:47:52.849153", "Another File", "etc. 1")
mi_2 = MultiItem("Local", 1579373292.452993, None, "This File", "etc. 2")
mi_3 = MultiItem("Remote", None, "2020-01-18T13:48:12.452993", "That File", "etc. 3")
file_list = [mi_0, mi_1, mi_2, mi_3]
file_list.sort()
from pprint import pprint
pprint(file_list)
# only the __lt__() method is required to implement to enable sorting
# __gt__(), __eq__(), __ne__(), __ge__(), __le__() methods: < > == != >= <=
# can get them all by implementing __lt__() and __eq__(), then applying
# the `@total_ordering` class decorator
from functools import total_ordering

@total_ordering
@dataclass(frozen=True)
class MultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

    def __lt__(self, other: "MultiItem") -> bool:
        return self.datetime < cast(MultiItem, other).datetime

    def __eq__(self, other: object) -> bool:
        return self.datetime == cast(MultiItem, other).datetime

    @property
    def datetime(self) -> datetime.datetime:
        if self.data_source == "Local":
            return datetime.datetime.fromtimestamp(
                cast(float, self.timestamp))
        else:
            return datetime.datetime.fromisoformat(
                cast(str, self.creation_date))

@dataclass(frozen=True)
class SimpleMultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

    def by_timestamp(item: "SimpleMultiItem") -> datetime.datetime:
        if self.data_source == "Local":
            return datetime.datetime.fromtimestamp(
                cast(float, self.timestamp))
        elif item.data_source == "Remote":
            return datetime.datetime.fromisoformat(
                cast(str, self.creation_date))
        else:
            raise ValueError(f"Unknown data_source in {item!r}")
# it is common to sort a list of tuples by something other than first item in
# the list the `operator.attrgetter` method canbe sued as a key to do this
'''??? file_list.sort(key=by_timestamp)'''
file_list.sort(key=lambda item: item.name)
import operator
file_list.sort(key=operator.attrgetter("name"))
# the `attrgetter()` function fetches a specific attribute from an object
# with tuples or dicts, `itemgetter()` can be used to extract a specific item by
# name or position; `methodcaller()`, which returns the result of a method call
# on the object being sorted;

""" Sets """
# sets are inherently unordered due to a hash-based data structure used for
# efficient access to the members; therefore sets cannot have items looked up
# by index; for sorting convert the set to a list;
song_library = [
    ("Phantom Of The Opera", "Sarah Brightman"),
    ("Knocking On Heaven's Door", "Guns N' Roses"),
    ("Captain Nemo", "Sarah Brightman"),
    ("Patterns In The Ivy", "Opeth"),
    ("November Rain", "Guns N' Roses"),
    ("Beautiful", "Sarah Brightman"),
    ("Mal's Song", "Vixy and Tony"),
]
artists = set()
for song, artist in song_library:
    artists.add(artist)
print(artists, "Opeth" in artists)
alphabetical = list(artists)
alphabetical.sort()
print(alphabetical)
# the primary feature of a set is uniqueness; sets are often used to deduplicate
# data, to create combinations, unions and differences between collections;
# `union` method == logical `or` operation
# `intersection` method == logical `and` operation
# `symmetric_difference` method == the `^` operator
dusty_artists = {"Yes", "Guns N' Roses", "Genesis"}
print(f"All: {dusty_artists | artists}")
print(f"Both: {dusty_artists.intersection(artists)}")
print(f"Either but not both: {dusty_artists ^ artists}")
# the union, intersection, and symmetric difference methods are commutative
# `issubset` and `issuperset` -> bool:
# `issubset` method returns True fi all of the items in the calling set are also
# in the set passed as an argument; the `<=` operator;
# `issuperset` method returns True if all of the items in the argument are also
# in the calling set; the inverse of `issubset`
# `difference` method returns all the elements that are in the calling set, but
# not in the set passed as an argument; the `-` operator;
print( artists.issuperset(dusty_artists),
        artists.issubset(dusty_artists),
        artists - dusty_artists,
        dusty_artists.difference(artists) )
# The `union`, `intersection`, and `difference` methods can all take multiple
# sets as arguments; they will return, as we might expect, the set that is
# created when the operation is called on all the parameters.
# !!! sets are much more efficient than lists when checking for membership
# using the `in` keyword !!!

""" 3 types of queues """
# a `queue` is a special kind of buffer, summarized as First In First Out (FIFO)
# the idea is to act as a temporary stash so one part of an application can write
# to the queue while another part consumes items from the queue;
from typing import List
from pathlib import Path

class ListQueue(List[Path]):
    # 1. List using the pop() and append() methods of a list;
    def put(self, item: Path) -> None:
        self.append(item)
    def get(self) -> Path:
        return self.pop(0)
    def empty(self) -> bool:
        return len(self) == 0
# 2. the `collections.deque` structure, which supports popleft() and append()
# methods; a "deque" is a Double-Ended Queue;
from typing import Deque

class DeQueue(Deque[Path]):
    def put(self, item: Path) -> None:
        self.append(item)
    def get(self) -> Path:
        return self.popleft()
    def empty(self) -> bool:
        return len(self) == 0
# 3. the `queue` module provides a queue often used for multithreading, but it
# can also be used for our single thread to examine a directory tree; get(), put()
import queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    BaseQueue = queue.Queue[Path]   # for mypy
else:
    BaseQueue = queue.Queue     # used at runtime

class ThreadQueue(BaseQueue):
    pass
#
