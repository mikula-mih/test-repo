from __future__ import annotations
# As with Python's data structures, most of these tools are syntactic sugar over
# an underlying object-oriented implementation; think of them as a further
# abstraction layer built on top of the (already abstracted) object-oriented
# paradigm.

""" Python built-in functions """
# there are numerous functions that perform a task or calculate a result on
# certain types of objects without being methods on the underlying class;
# `len()` function
obj = [1, 2, 3]
print(len(obj), obj.__len__())
# `reversed()` function:
# takes any sequence as input and returns a copy of that sequence in reverse
# order; it is normally used in for statements when we want to iterate over
# items from back to front;
class CustomSequence:
    def __init__(self, args):
        self._list = args
    def __len__(self):
        return 5
    def __getitem__(self, index):
        return f"x{index}"

class FunkyBackwords(list):
    def __reversed__(self):
        return "BACKWARDS!"

generic = [1, 2, 3, 4, 5]
custom = CustomSequence([6, 7, 8, 9, 10])
funkadelic = FunkyBackwords([11, 12, 13, 14, 15])

for sequence in generic, custom, funkadelic:
    print(f"{sequence.__class__.__name__}: ", end="")
    for item in reversed(sequence):
        print(f"{item}", end="")
    print()
# `enumerate()` function
# creates a sequence of tuples, where the first object in each tuple is the
# index and the second is the original item;
from pathlib import Path
with Path("OOP.md").open() as source:
    for index, line in enumerate(source, start=1):
        print(f"{index:3d}: {line.rstrip()}")
# the `enumerate` function is an iterable: it returns a sequence of tuples;
# `abs()`, `str()`, `repr()`, `pow()`, `divmod()` map directly to the special
# methods __abs__(), __str__(), __repr__(), __pow__(), __divmod__();
# `bytes()`, `format()`, `hash()`, `bool()` also map directly to the special
# methods __bytes__(), __format__(), __hash__(), __bool__()
#
# `all()` and `any()`, which accept an iterable object and return True if all,
# or any, of the items evaluate to true (such as a non-empty string or list, a
# non-zero number, an object that is not None, or the literal True);
#
# `eval()`, `exec()`, and `compile()`, which execute string as code inside the
# interpreter;
#
# `hasattr()`, `getattr()`, `setattr()`, and `delattr()`, which allow attributes
# on an object to be manipulated by their string names;
#
# `zip()`, which takes two or more sequences and returns a new sequence of
# tuples, where each tuple contains a single value from each sequence;
#
# help("builtins")

""" an alternative to method overloading """
# `method overloading`:
# refers to having multiple methods with the same name that accept different
# sets of parameters;
# `typing.Union` hint to show that a parameter can have values from Union[int, str]
from typing import Any, Optional
def mandatory_params(x: Any, y: Any, z: Any) -> str:
    return f"{x=}, {y=}, {z=}"

""" Default values for parameters """
def latitude_dms(
    deg: float, min: float, sec: float = 0.0, dir: Optional[str] = None
) -> str:
    if dir is None:
        dir = "N"
    return f"{deg:02.0f}° {min+sec/60:05.3f}{dir}"

print(latitude_dms(36, 51, 2.9, "N"))
# `keyword-only` parameter:
# placing a * before all of the keyword-only parameters
def kw_only(
    x: Any, y: str = "defaultkw", *, a: bool, b: str = "only"
) -> str:
    return f"{x=}, {y=}, {a=}, {b=}"

print(kw_only('x', a='a', b='b'))
# mark parameters as being supplied only by position:
# providing these names before a single / that separates the positional-only
# parameters from the more flexible parameters that follow
def pos_only(x: Any, y: str, /, z: Optional[Any] = None) -> str:
    return f"{x=}, {y=}, {z=}"

print(pos_only(2, "three"))

""" Additional details on defaults """
# we can't have dynamically generated default values
number = 5
def funky_function(x: int = number) -> str:
    return f"{x=}, {number=}"
# the current value when the function is defined
print(funky_function(42), "\n", funky_function())
# uses the current value of a global number variable
def better_function(x: Optional[int] = None) -> str:
    if x is None:
        x = number
    return f"better: {x=}, {number=}"

def better_function_2(x: Optional[int] = None) -> str:
    x = number if x is None else x
    return f"better: {x=}, {number=}"
# The "evaluation at definition time" can trip us up when working with mutable
# containers such as lists, sets, and dictionaries
from typing import List

def good_default(
    tag: str, history: Optional[list[str]] = None
) -> list[str]:
    history = [] if history is None else history
    history.append(tag)
    return history

""" Variable argument lists """
from urllib.parse import urlparse
from pathlib import Path

def get_pages(*links: str) -> None:
    for link in links:
        url = urlparse(link)
        name = "index.html" if url.path in ("", "/") else url.path
        target = Path(url.nerloc.replace(".", "_")) / name
        print(f"Create {target} from {link!r}")
# The * in the *links parameter says, I'll accept any number of arguments and
# put them all in a tuple named links;
from typing import Dict, Any

class Options(Dict[str, Any]):
    default_options: dict[str, Any] = {
        "port": 21,
        "host": "localhost",
        "username": None,
        "password": None,
        "debug": False,
    }

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(self.default_options)
        self.update(kwargs)
#
import contextlib
import os
import subprocess
import sys
from typing import TextIO
from pathlib import Path

def doctest_everything(
    output: TextIO,
    *directories: Path,
    verbose: bool = False,
    **stems: str
) -> None:
    def log(*args: Any, **kwargs: Any) -> None:
        if verbose:
            print(*args, **kwargs)

    with contextlib.redirect_stdout(output):
        for directory in directories:
            log(f"Searching {directory}")
            for path in directory.glob("**/*.md"):
                if any(
                    parent.stem == ".tox"
                    for parent in path.parents
                ):
                    continue
                log(
                    f"File {path.relative_to(directory)}, "
                    f"{path.stem=}"
                )
                if stems.get(path.stem, "").upper() == "SKIP":
                    log("Skipped")
                    continue
                options = []
                if stems.get(path.stem, "").upper() == "ELLIPSIS":
                    options += ["ELLIPSIS"]
                search_path = directory / "src"
                print(
                    f"cd '{Path.cwd()}'; "
                    f"PYTHONPATH='{search_path}' doctest '{path}' -v"
                )
                option_args = (
                    ["-o", ",".join(options)] if options else []
                )
                subprocess.run(
                    ["python3", "-m", "doctest", "-v"]
                        + option_args + [str(path)],
                    cwd=directory,
                    env={"PYTHONPATH": str(search_path)},
                )
#
doctest_log = Path("doctest.log")
with doctest_log.open('w') as log:
    doctest_everything(
        log,
        Path.cwd() / "ch_04",
        Path.cwd() / "ch_05",
        verbose=True
    )
#
""" Unpacking arguments """
def show_args(arg1, arg2, arg3="THREE"):
    return f"{arg1=}, {arg2=}, {arg3=}"
# the * iperator inside a function call to unpack it into the three arguments
some_args = range(3)
show_args(*some_args)
# if we have a dictionary of arguments, we can use the ** syntax to unpack a
# dictionary to supply argument values for keyword parameters;
more_args = {
    "arg1": "ONE",
    "arg2": "TWO"}
show_args(**more_args)
#
def __init__(self, **kwargs: Any) -> None:
    super().__init__(self.default_options)
    self.update(kwargs)
#
def __init__(self, **kwargs: Any) -> None:
    super().__init__({**self.default_options, **kwargs})
# this dictionary unpacking is a handy consequence of the way the ** operator
# transforms a dictionary into named parameters for a function call;
x = {'a': 1, 'b': 2}
y = {'b': 11, 'c': 3}
z = {**x, **y}  # {'a': 1, 'b': 11, 'c': 3}
# Python considers functions as one kind of "callabe" object; this means functions
# are objects, and higher-order functions can accept functions as argument values
# and return functions as results;
'''Functions are objects'''
def fizz(x: int) -> bool:
    return x % 3 == 0
def buzz(x: int) -> bool:
    return x % 5 == 0
def name_or_number(
    number: int, *tests: Callable[[int], bool]) -> None:
    for t in tests:
        if t(number):
            return t.__name__
    return str(number)

for i in range(1, 11):
     print(name_or_number(i, fizz, buzz))

'''Function objects and callbacks'''
import heapq
import time
from typing import Callable, Any, List, Optional
from dataclasses import dataclass, field

Callback = Callable[[int], None]

@dataclass(frozen=True, order=True)
class Task:
    scheduled: int
    callback: Callback = field(compare=False)
    delay: int = field(default=0, compare=False)
    limit: int = field(default=1, compare=False)

    def repeat(self, current_time: int) -> Optional["Task"]:
        if self.delay > 0 and self.limit > 2:
            return Task(
                current_time + self.delay,
                cast(Callback, self.callback), # type: ignore [misc]
                self.delay,
                self.limit - 1,
            )
        elif self.delay > 0 and self.limit == 2:
            return Task(
                current_time + self.delay,
                cast(Callback, self.callback), # type: ignore [misc]
            )
        else:
            return None
#
class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def enter(
        self,
        after: int,
        task: Callback,
        delay: int = 0,
        limit: int = 1,
    ) -> None:
        new_task = Task(after, task, delay, limit)
        heapq.heappush(self.tasks, new_task)

    def run(self) -> None:
        current_time = 0
        while self.tasks:
            next_task = heapq.heappop(self.tasks)
        if (delay := next_task.scheduled - current_time) > 0:
            time.sleep(next_task.scheduled - current_time)
        current_time = next_task.scheduled
        next_task.callback(current_time) # type: ignore [misc]
        if again := next_task.repeat(current_time):
            heapq.heappush(self.tasks, again)
#
import datetime

def format_time(message: str) -> None:
    now = datetime.datetime.now()
    print(f"{now:%I:%M:%S}: {message}")
def one(timer: float) -> None:
    format_time("Called One")
def two(timer: float) -> None:
    format_time("Called Two")
def three(timer: float) -> None:
    format_time("Called Three")
class Repeater:
    def __init__(self) -> None:
        self.count = 0
    def four(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")
#
'''Using functions to patch a class'''
class A:
    def show_something(self):
        print("My class is A")

def patched_show_something():
    print("My class is NOT A")

a_object = A()
a_object.show_something()   # >>> My class is A
a_object.show_something = patched_show_something
a_object.show_something()   # >>> My class is NOT A
# `monkey patching`: replacing or adding methods at runtime is used in
# automated testing;
# this kind of code `tech debt`, because the complication of using a monkey
# patch is a liability;
""" Callable object """
# just as functions are objects that can have attributes set on them, it is
# possible to create an object that can be called as though it were a function;
# any object can be made callable by giving it a `__call__()` method that
# accepts the required arguments;
class Repeater_2:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")

rpt = Repeater_2()
rpt(1)  # Called Four: 1
# An ordinary function is stateless. A callable object can be stateful;
# some algorithms can have a dramatic performance improvement from saving results
# in cache, and a callable object is a great way to save results from a function
# so they don't need to be recomputed;

""" File I/O """
with open("file.txt") as input:
    for line in input:
        print(line)
#
results = str(2**2048)
with open("big_file.txt", "w") as output:
    output.write("# A big number\n")
    output.writelines(
        [
            f"{len(results)}\n",
            f"{results}\n"
        ]
    )
#
source_path = Path("requirements.txt")
with source_path.open() as source_file:
    for line in source_file:
        print(line, end='')
#
class StringJoiner(list):
    def __enter__(self):
        return self
    def __exit(self, exc_type, exc_val, exc_tb):
        self.result = "".join.(self)
#
from typing import List, Optional, Type, Literal
from types import TracebackType

class StringJoiner(List[str]):
    def __enter__(self) -> "StringJoiner":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        self.result = "".join(self)
        return False
#
with StringJoiner("Hello") as sj:
    sj.append(", ")
    sj.extend("world")
    sj.append("!")
print(sj.result)   # >>> 'Hello, world!'
#
class StringJoiner2(List[str]):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)
        self.result = "".join(self)

from contextlib import contextmanager
from typing import List, Any, Iterator

@contextmanager
def joiner(*args: Any) -> Iterator[StringJoiner2]:
    string_list = StringJoiner2(*args)
    try:
        yield string_list
    finally:
        string_list.result = "".join(string_list)
#
