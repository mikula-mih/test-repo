

def plain_class_example():
    class T:
        def __init__(self, n: int, f: float, s: str):
            self.n = n
            self.f = f
            self.s = s

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')
    y = x.n
    x.n = 0

def dataclass_example():
    from dataclasses import dataclass
    # built-in dataclass decoretor
    @dataclass(slots=True)  # Python3.10
    class T:
        n: int
        f: float
        s: str

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')
    y = x.n
    x.n = 0

# alternitive to dataclass is `attr`
def attr_class_example():
    import attr

    @attr.s
    class T:
        n: int = attr.ib(convert=int)  # verbose
        f: float = attr.ib(validator=attr.validators.instance_of(float))
        s: str = attr.ib(default="")
        l: list = attr.ib(default_factory=list)

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')
    # can convert or validate but not required

    y = x.n
    x.n = 0


def tuple_example():
    x = 42, 4.5, 'hello'
    y = x[0]    # access by index error-prone
    # immutable

def namedtuple_example():
    from collections import namedtuple

    T = namedtuple('T', ['n', 'f', 's'])

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')

    y = x[0]
    y = x.n
    # immutable

def NamedTuple_example():
    from typing import NamedTuple
    # major draw back: they are based of typles
    class T(NamedTuple): # easier to read
        n: int  # type hints available
        f: float
        s: str
    # immutable-> you'd have to make a copy of a typle with a different value
    # in a typle in one of the slots
    # new instance creation for changing values
    # type safty - ?

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')

    y = x[0]
    y = x.n
    # immutable

def dict_example():
    x = {
        'n': 42,
        'f': 4.5,
        's': 'hello'
    }
    y = x['n']  # access by str error-prone
    x['n'] = 0

def SimpleNameSpace_example():
    from types import SimpleNamespace # just like object
    # it allows you to set attributes on it at runtime, whereas object doesn't
    x = SimpleNamespace(n=42, f=4.5, s='hello') # must be kwargs

    y = x.n
    x.n = 0

def pydantic_example():
    # !!! parsing, not a general purpose
    from pydantic import BaseModel
    # By default, pydantic will try to convert things into these types when
    # you construct this object or set an attribute;
    # Ant it will check those types at runtime;
    class T(BaseModel): # You might consider static type chacking -> catching
    # errors before program even runs;
        n: int
        f: float
        s: str
    # One of the common problems that you get when you're parsing data is that
    # the data you're reading might not be valid or it might not be in the right
    # format; So, converting things at runtime and checking types and conversions
    # at runtime makes a lot of sense for the specific task of parsing;
    # However, doing all this at runtime is a huge waste fo resources, both time
    # and memory, if parsing is not your goal;
    x = T(n=42, f=4.5, s='hello')   # must be kwargs
    y = x.n
    x.n = 0
    # args always converted to given types, type-checked at
