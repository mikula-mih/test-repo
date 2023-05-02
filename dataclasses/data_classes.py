import random
import string
from dataclasses import dataclass, field


def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))


class PersonSimple:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    # def __str__(self) -> str:
    #     return f"{self.name}, {self.address}"

def main_0() -> None:
    person = PersonSimple(name="John", address="123 Main St")
    print(person.__dict__["name"])
    print(person)


# @dataclass(kw_only=True)
# @dataclass(slots=True)
# @dataclass(frozen=True) == once initialize can't be changed
@dataclass
class Person:
    name: str
    address: str
    active: bool = True
    email_addresses: list[str] = field(default_factory=list)
    id: str = field(init=False, default_factory=generate_id)
    _search_string: str = field(init=False, repr=False)
    # generate value from another instance variables
    def __post_init__(self) -> None:
        self._search_string = f"{self.name} {self.address}"

# `slots` are faster than `__dict__`
@dataclass(slots=True)
class PersonSlots:
    name: str
    address: str
    email: str

# !!! dont use `slots` with multiple inheritances !!!
class PesonMultiple(Person, PersonSlots):
    pass


def get_set_delete(person: Person | PersonSlots):
    person.address = "123 Main St"
    person.address
    del person.address


def main():
    person = Person("John", "123 Main St", "john@doe.com")
    person.name = "Sobebody"
    person_slots = PersonSlots("John", "123 Main St", "john@doe.com")
    print(person)
    no_slots = min(timeit.repeat(partial(get_set_delete, person), number=1000000))
    slots = min(timeit.repeat(partial(get_set_delete, person_slots), number=1000000))
    print(f"No slots: {no_slots}")
    print(f"Slots: {slots}")
    print(f"% performance improvement: {(no_slots - slots) / no_slots:.2%}")


if __name__ == "__main__":
    import timeit
    from functools import partial
    main_0()
    main()
