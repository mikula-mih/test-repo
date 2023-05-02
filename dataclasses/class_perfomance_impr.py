
# `Descriptor` - is an attribute value that has one of the methods in the
#   descriptor protocol: get, set, delete dunder methods; (implemented in C)
import timeit
from dataclasses import dataclass
from functools import partial

# Slots hav some limitations;
# `mixins` and `multiple inheritance`; cant combine classes that use slots

class Person:
    def __init__(self, name: str, address: str, email: str):
        self.name = name
        self.address = address
        self.email = email


class PersonSlots:
    __slots__ = "name", "address", "email"

    def __init__(self, name: str, address: str, email: str):
        self.name = name
        self.address = address
        self.email = email


def get_set_delete(person: Person | PersonSlots):
    person.address = "123 Main St"
    _ = person.address
    del person.address


def main():
    person = Person("John", "123 Main St", "john@doe.com")
    print(person.__dict__)
    person.hi = "hello"
    print(person.__dict__)
    del person.hi
    print(person.__dict__)

    person_slots = PersonSlots("John", "123 Main St", "john@doe.com")
    no_slots = min(timeit.repeat(partial(get_set_delete, person), number=1_000_000))
    slots = min(timeit.repeat(partial(get_set_delete, person_slots), number=1_000_000))

    print(f"No slots: {no_slots}")
    print(f"Slots: {slots}")
    print(f"% performance improvement: {(no_slots - slots) / no_slots:.2%}")


def main_with_dataclasses_and_slots():

    @dataclass(slots=False)
    class Person:
        name: str
        address: str
        email: str

    @dataclass(slots=True)
    class PersonSlots:
        name: str
        address: str
        email: str

    person = Person("John", "123 Main St", "john@doe.com")
    person_slots = PersonSlots("John", "123 Main St", "john@doe.com")
    no_slots = min(timeit.repeat(partial(get_set_delete, person), number=1_000_000))
    slots = min(timeit.repeat(partial(get_set_delete, person_slots), number=1_000_000))

    print(f"No slots: {no_slots}")
    print(f"Slots: {slots}")
    print(f"% performance improvement: {(no_slots - slots) / no_slots:.2%}")



def main_error_with_slots():
    @dataclass(slots=False)
    class Employee:
        dept: str


    @dataclass(slots=True)
    class EmployeeSlots:
        dept: str


    # uncomment the class below that uses multiple inheritance and see the error
    # class PersonEmployee(PersonSlots, EmployeeSlots):
    #    pass

    class PersonNewSlots:
        # can do multiple inheritances by adding __dict__
        __slots__ = "name", "address", "email", "__dict__"

        def __init__(self, name: str, address: str, email: str):
            self.name = name
            self.address = address
            self.email = email


    class EmployeeNewSlots:
        __slots__ = ("dept",)

        def __init__(self, dept: str):
            self.dept = dept


    # uncomment the class below that uses multiple inheritance and see the error
    # class PersonEmployee(PersonNewSlots, EmployeeNewSlots):
    #     pass


if __name__ == "__main__":
    main()
    main_with_dataclasses_and_slots()
    main_error_with_slots()
