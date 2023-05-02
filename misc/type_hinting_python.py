
- NamedTuple
- dataclass
- TypedDict
- Enum
- Literal
- Union, Optional
- Iterable, Sequence
- Callable
- TypeVar

# mypy
# >>> pip install mypy
# >>> mypy *.py
# Optional
def print_hello(name: str | None=None) -> None:
    print(f"Hello, {name}" if name is not None else "hello anon!")
# Containers
# # Iterable, Sequence, Mapping etc.
from datatime import datetime
from dataclasses import dataclass
from typing import Iterable, Sequence, Mapping

@dataclass
class User:
    birthday: datetime

users = [
    User(birthday=datetime.fromisoformat("1988-01-01")),
    User(birthday=datetime.fromisoformat("1988-01-01")),
    User(birthday=datetime.fromisoformat("1988-01-01"))
]

def get_younger_user(users: Iterable[User]) -> User:
    if not users: raise ValueError("empty users!")
    sorted_users = sorted(users, key=lambda x: x.birthday)
    return sorted_users[0]

def get_younger_user_with_index_access(users: Sequence[User]) -> User:
    if not users: raise ValueError("empty users!")
    print(users[0])
    sorted_users = sorted(users, key=lambda x: x.birthday)
    return sorted_users[0]

def smth(some_users: Mapping[str, User]) -> None:
    print(some_users["alex"])

smth({
    "alex": User(birthday=datetime.fromisoformat("1988-01-01")),
    "petr": User(birthday=datetime.fromisoformat("1988-01-01"))
})
# tuples
int_tuple = tuple[int, ...]
def smth(wow: int_tuple): pass
# Generics
from typing import TypeVar, Iterable

T = TypeVar("T")

def first(iterable: Iterable[T]) -> T | None:
    for element in iterable:
        return element
# Callable
from typing import Callable

def mysum(a: int, b: int) -> int:
    return a + b

def process_operation(operation: Callable[[int, int], int],
                        a: int, b: int) -> int:
    return operation(a, b)
# stub files
# __init__.pyi
