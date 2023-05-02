from __future__ import annotations
# the `for` loop, which seems so structured, is actually a lightweight wrapper
# around a set of object-oriented principles;
# `Design pattern`:
# applied to solve a common problem faced by developers in some specific situation;
# a suggestion as to the ideal solution for that problem, in terms of object-
# oriented design;

""" the Iterator Pattern """
# the `iterator design pattern`
# an `iterator` is an object with a `next()` method and `done()` method;
# the latter returns True if there are no items left in the sequence;
while not iterator.done():
    item = iterator.next()
# the method gets a special name, `__next__`;
# it can be accessed using the `next(iterator)` built-in;
# Rather than a `done()` method, Python's iterator protocol raises the `StopIteration`
# exception to notify the client that the iterator has completed;
''' the `iterator protocol` '''
# the `Iterator` abstract base class, in the `collections.abc` module, defines
# the `iterator` protocol in Python;
# any `Collection` class definition must be `Iterable`:
# implementing an `__iter__()` method; this method creates an `Iterator` object;
# `__next__()` method calls to get a new element from the sequence;
from typing import Iterable, Iterator

class CapitalIterable(Iterable[str]):
    def __init__(self, string: str) -> None:
        self.string = string

    def __iter__(self) -> Iterator[str]:
        return CapitalIterator(self.string)

class CapitalIterator(Iterator[str]):
    def __init__(self, string: str) -> None:
        self.words = [w.capitalize() for w in string.split()]
        self.index = 0

    def __next__(self) -> str:
        if self.index == len(self.words):
            raise StopIteration()

        word = self.words[self.index]
        self.index += 1
        return word
#
iterable = CapitalIterable('the quick brown fox jumps over the lazy dog')
iterator = iter(iterable)
# 1st
while True:
    try:
        print(next(iterator))
    except StopIteration:
        break
# 2nd
for i in iterable:
    print(i)
# a regular expression has a method, `finditer()`, that is an iterator over each
# instance of a matching substring that it can find;
# the `Path.glob()` method will iterate over matching items in a directory;
# the `range()` object is also an iterator;
''' `Comprehensions` '''
# Comprehensions are simple, but powerful, syntaxes that allow us to transform
# or filter an iterable object in as little as one line of code.
# The resultant object can be a perfectly normal list, set, or dictionary,
# or it can be a generator expression that can be efficiently consumed
# while keeping just one element in memory at a time.
''' List comprehesions '''
input_strings = ["1", "5", "28", "131", "3"]
output_integers = []
for num in input_strings:
    output_integers.append(int(num))
#
output_integers = [int(num) for num in input_strings]
# Terminology-wise, we call this a `mapping`. Applying the result expression to
# map values from the source iterable to create a resulting iterable list;
output_integers = [int(num) for num in input_strings if len(num) < 3]
# `filter`: exclude values by adding an `if` statement inside the comprehesion;
from pathlib import Path
# text files are iterable; each call to `__next__()` on the file's iterator will
# return one line of the file;
source_path = Path('src') / 'iterator_protocol.py'
with source_path.open() as source:
    exaples = [line.rstrip()
        for line in source
        if ">>>" in line]
# the built-in `enumerate()` function helps us pair a number with each item
# provided by the iterator;
with source_path.open() as source:
    example = [(number, line.rstrip())
        for number, line in enumerate(source, start=1)
        if ">>>" in line]
# the `enumerate()` function consumes an iterable, providing an iterable
# sequence of two-tuples of a number and the original item;
''' Set & dictionary comprehesions '''
from typing import NamedTuple
class Book(NamedTuple):
    author: str
    title: str
    genre: str

books = [
    Book("Pratchett", "Nightwatch", "fantasy"),
    Book("Pratchett", "Thief Of Time", "fantasy"),
    Book("Le Guin", "The Dispossessed", "scifi"),
    Book("Le Guin", "A Wizard Of Earthsea", "fantasy"),
    Book("Jemisin", "The Broken Earth", "fantasy"),
    Book("Turner", "The Thief", "fantasy"),
    Book("Phillips", "Preston Diamond", "western"),
    Book("Phillips", "Twice Upon A Time", "scifi"),
]
fantasy_authors = {b.author for b in books if b.genre == "fantasy"}
#
''' Generator expressions '''
# they use the same syntax as comprehensions, but don't create a final container
# object; they are called `lazy`; they reluctuntly produce values on demand;
# to create a generator expression, wrap the comprehension in ();
full_log_path = Path.cwd() / "data" / "sample.log"
warning_log_path = Path.cwd() / "data" / "warnings.log"

with full_log_path.open() as source:
    warning_lines = (line for line in source if "WARN" in line)
    with warning_log_path.open('w') as target:
        for line in warning_lines:
            target.write(line)
# the core of a comprehesion is the generator expression;
# Wrapping a generator in [] creates a list; in {} creates a set;
# Using {} and : to separate keys and values creates a dictionary;
# Wrapping a generator in() is still a generator expression, not a tuple;
''' Generator functions '''
import csv
import re
from pathlib import Path
from typing import Match, cast

def extract_and_parse_1(
    full_log_path: Path, warning_log_path: Path
) -> None:
    with warning_log_path.open("w") as target:
        writer = csv.writer(target, delimiter="\t")
        pattern = re.compile(
            r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
        with full_log_path.open() as source:
            for line in source:
                if "WARN" in line:
                    line_groups = cast(
                        Match[str], pattern.match(line)).groups()
                    writer.writerow(line_groups)
#
from typing import Match, cast, Iterator, Tuple, TextIO

class WarningReformat(Iterator[Tuple[str, ...]]):
    pattern = re.compile(
        r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")

    def __init__(self, source: TextIO) -> None:
        self.insequence = source

    def __iter__(self) -> Iterator[tuple[str, ...]]:
        return self

    def  __next__(self) -> tuple[str, ...]:
        line = self.insequence.readline()
        while line and "WARN" not in line:
            line = self.insequence.readline()
        if not line:
            raise StopIteration
        else:
            return tuple(
                cast(Match[str],
                    self.pattern.match(line)
                ).groups()
            )

def extract_and_parse_2(
    full_log_path: Path, warning_log_path: Path
) -> None:
    with warning_log_path.open("w") as target:
        writer = csv.writer(target, delimiter="\t")
        with full_log_path.open() as source:
            filter_reformat = WarningReformat(source)
            for line_groups in filter_reformat:
                writer.writerow(line_groups)
#
warnings_filter = (
    tuple(cast(Match[str], pattern.match(line)).groups())
    for line in source
    if "WARN" in line
)
''' `Yield` items from another iterable '''
def file_extract(
    path_iter: Iterable[Path]
) -> Iterator[tuple[str, ...]]:
    for path in path_iter:
        with path.open() as infile:
            yield from warnings_filter(infile)

def extract_and_parse_d(
        directory: Path, warning_log_path: Path) -> None:
    with warning_log_path.open("w") as target:
        writer = csv.writer(target, delimiter="\t")
        log_files = list(directory.glob("sample*.log"))
        for line_groups in file_extract(log_files):
            writer.writerow(line_groups)
#
''' Generator stacks '''
def warnings_filter(source: Iterable[str]
) -> Iterator[Sequence[str]]:
    pattern = re.compile
        (r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")
    for line in source:
        if match := pattern.match(line):
            if "WARN" in match.group(2):
                yield match.groups()
#
possible_match_iter = (pattern.match(line) for line in source)
group_iter = (
    match.groups() for match in possible_match_iter if match)
warnings_filter = (
    group for group in group_iter if "WARN" in group[1])
#
possible_match_iter = (
    pattern.match(line) for line in source)
group_iter = (
    match.groupdict() for match in possible_match_iter if match)
warnings_iter = (
    group for group in group_iter if "WARN" in group["level"])
dt_iter = (
    (
        datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
        g["level"],
        g["msg"],
    )
    for g in warnings_iter
)
warnings_filter = (
    (g[0].isoformat(), g[1], g[2]) for g in dt_iter)
#
possible_match_iter = map(pattern.match, source)
good_match_iter = filter(None, possible_match_iter)
group_iter = map(lambda m: m.groupdict(), good_match_iter)
warnings_iter = filter(lambda g: "WARN" in g["level"], group_iter)
dt_iter = map(
    lambda g: (
        datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
        g["level"],
        g["msg"],
    ),
    warnings_iter,
)
warnings_filter = map(
    lambda g: (g[0].isoformat(), g[1], g[2]), dt_iter)
#
