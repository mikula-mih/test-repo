from __future__ import annotations
# to use the generic types as annotations
# Generic collections: set[something], list[something], dict[key, value]
from typing import List, Protocol

"""All Python classes are subclasses of the special built-in class named object.
    This class provides a little bit of metadata & a few built-in behaviors"""
class MySubClass(object):   # subclass: MySubClass, inherits from superclass
    # A subclass is also said to be derived from its parent class,
    # or the subclass extends the parent class
    pass
"""The `superclasses`, or `parent classes`,
    in the relationship are the classes that are being inherited from"""

class Contact:
    all_contacts: List["Contact"] = []  # class variable
    # we can also access it as self.all_contacts from within any method on
    # an instance of the Contact class

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}"
            f")"
        )

c_1 = Contact("Dusty", "dusty@example.com")
c_2 = Contact("Steve", "steve@example.com")
# If you ever attempt to `set` the variable using self.all_contacts, you will
# actually be creating a new instance variable associated just with that object
Contact.all_contacts

class Supplier(Contact):
    def order(self, order: "Order") -> None:
        print(
            "If this were a real system we would send "
            f"'{order}' order to '{self.name}'"
        )

s = Supplier("Sup Plier", "supplier@example.net")
print(s.name, s.email)

from pprint import pprint
pprint(s.all_contacts)
s.order("I need pliers")

"""Extending built-ins"""
# inheritance from a built-in type: list.
# our list is only of instances of the Contact class by: list["Contact"]
"""from __future__ import annotations
for this syntax to work in Python 3.9

typing.NamedTuple definition lets us define new kinds of immutable tuples
    and provides useful names for the members.
typing.TextIO or typing.BinaryIO hints for a new kind of file to describe
    built-in file operations.
typing.Text by extending it to create new types of strings
"""
# Instead of instantiating a generic list as our class variable
class ContactList(list["Contact"]): # create a new class that extends list type
    def search(self, name: str) -> list["Contact"]:

        matching_contacts: list["Contact"] = []
        for contact in self:
            if name in contact.name:
                matching_contacts.append(contact)
        return matching_contacts

# instantiate this subclass as our all_contacts list.
class Contact():
    all_contacts = ContactList()

    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email
        Contact.all_contacts.append(self)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.email!r}" f")"
        )

c1 = Contact("John A", "johna@example.net")
c2 = Contact("John B", "johnb@sloop.net")
c3 = Contact("Jenna C", "cutty@sark.io")
print(*(c.name for c in Contact.all_contacts.search('John')))


class LongNameDict(dict[str, int]):
    def longest_key(self) -> Optional[str]:
        """In effect, max(self, key=len), but less obscure"""
        longest = None
        for key in self:
            if longest is None or len(key) > len(longest):
                longest = key
        return longest

articles_read = LongNameDict()
articles_read['lucy'], articles_read['c_c_phillips'] = 42, 6
print(articles_read.longest_key() == max(articles_read, key=len))   # True

"""Overriding & super"""
# Overriding means altering or replacing a method of the superclass with
# a new method (with the same name) in the subclass.
class Friend(Contact):
    def __init__(self, name: str, email: str, phone: str) -> None:
        # super() function returns the object as if it was actually an instance
        # of the parent class, allowing us to call the parent method directly
        super().__init__(name, email)
        # first binds the instance to the parent class using super()
        # then calls __init__() on that object, passing in the expected arguments.
        self.phone = phone
# super() call can be made inside any method, at any point in the method
# for example, we may need to manipulate or validate incoming parameters before
# forwarding them to the superclass.

""" Multiple inheritance """
# `protocol` is a kind of incomplete class;
# `protocols` can have methods, class-level attribute names with type hints,
# but not full assignment statements
class Emailable(Protocol):
    email: str

""" mixin - design pattern """
# aspects of the host class for a mixin, & new aspects the mixin provides to the host
class MailSender(Emailable):
    def send_mail(self, message: str) -> None:
        print(f"Sending mail to {self.email=}")
        # Add e-mail logic here

class EmailableContact(Contact, MailSender):
    pass

e = EmailableContact(c1.name, c1.email)
print(Contact.all_contacts)
e.send_mail("lol")
# naive AddressHolder class; it doesn't account for multiple inheritance well
class AddressHolder:
    def __init__(self, street: str, city: str, state: str, code: str) -> None:
        self.street = street
        self.city = city
        self.state = state
        self.code = code

""" the Diamond Problem """
# naive approach
class Friend(Contact, AddressHolder):
    def __init__(
        self,
        name: str,
        email: str,
        phone: str,
        street: str,
        city: str,
        state: str,
        code: str,
    ) -> None:
        Contact.__init__(self, name, email)
        AddressHolder.__init__(self, street, city, state, code)
        self.phone = phone

""" diamond inheritance """
# the base class's call_me() method being called twice
class BaseClass:
    num_base_calls = 0

    def call_me(self) -> None:
        print("Calling method on BaseClass")
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    num_left_calls = 0

    def call_me(self) -> None:
        BaseClass.call_me(self) # USE super() insted
        # super().call_me()
        print("Calling method on LeftSubclass")
        self.num_left_calls += 1

class RightSubclass(BaseClass):
    num_right_calls = 0

    def call_me(self) -> None:
        BaseClass.call_me(self)
        # super().call_me()
        print("Calling method on RightSubclass")
        self.num_right_calls += 1

class Subclass(LeftSubclass, RightSubclass):
    num_sub_calls = 0

    def call_me(self) -> None:
        LeftSubclass.call_me(self)
        RightSubclass.call_me(self)
        # super().call_me()
        print("Calling method on Subclass")
        self.num_sub_calls += 1

Subclass().call_me()
# Python's `Method Resolution Order (MRO)` algorithm transforms the diamond into
# a flat, linear tuple. See the result of this in the __mro__ attribute of a class.
pprint(Subclass.__mro__)
# the `cooperative multiple inheritance` approach
# is to accept keyword arguments for any parameters that are not required
# by every subclass implementation
class Contact:
    all_contacts = ContactList()
    # special param `/` separates params that could be provided by position in
    # the call from params that require a keyword to associate them with arg value
    def __init__(self, /, name: str = "", email: str = "", **kwargs: Any) -> None:
        # extra param are passed up to the next class with the super() call
        super().__init__(**kwargs)  # type: ignore [call-arg]
        # **kwargs param collects all additional keyword arg value into dict
        self.name = name
        self.email = email
        self.all_contacts.append(self)

    def __repr__(self) -> str:
        return f""

class AddressHolder:
    def __init__(
        self,
        /,
        street: str = "",
        city: str = "",
        state: str = "",
        code: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs) # type: ignore [call-arg]
        self.street = street
        self.city = city
        self.state = state
        self.code = code

class Friend(Contact, AddressHolder):
    def __init__(self, /, phone: str = "", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.phone = phone
# the # type: ignore comments provide a specific error code,
# call-arg, on a specific line to be ignored
""" Polymorphism """
# different behaviors happen depending on which subclass is being used,
# without having to explicitly know what the subclass actually is
# the `Liskov Substitution Principle`
# We should be able to substitute any subclass for its superclass.
from pathlib import Path

class AudioFile:
    ext: str
    def __init__(self, filepath: Path) -> None:
        if not filepath.suffix == self.ext:
            raise ValueError("Invalid file format")
        self.filepath = filepath

class MP3File(AudioFile):
    ext = ".mp3"
    def play(self) -> None:
        print(f"playing {self.filepath} as mp3")

class WavFile(AudioFile):
    ext = ".wav"
    def play(self) -> None:
        print(f"playing {self.filepath} as wav")

class OggFile(AudioFile):
    ext = ".ogg"
    def play(self) -> None:
        print(f"playing {self.filepath} as ogg")

# Duck typing in Python allows us to use any object that provides
# the required behavior without forcing it to be a subclass
class FlacFile:
    def __init__(self, filepath: Path) -> None:
        if not filepath.suffix == ".flac":
            raise ValueError("Not a .flac file")
        self.filepath = filepath

    def play(self) -> None:
        print(f"playing {self.filepath} as flac")

# In some cases, we can formalize this kind of duck typing using
# a typing.Protocol hint. To make mypy aware of the expectations, we'll often
# define a number of functions or attributes (or a mixture) as a formal Protocol type.
class Playable(Protocol):
    def play(self) -> None:
        pass
# More succinctly, duck typing doesn't need to provide the entire interface
# of an object that is available;
# it only needs to fulfill the protocol that is actually used.
