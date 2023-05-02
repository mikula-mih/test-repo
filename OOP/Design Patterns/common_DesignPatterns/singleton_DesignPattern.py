
from typing import Iterable, cast
#
import state_DesignPattern
from state_DesignPattern import Message
# don't use in Python;
""" the `Singleton` pattern """
# the basic idea behind the `Singleton` pettern is to allow exactly
# one instance of a certain object to exist; such manager objects often need to
# be referenced by a wide variety of other objects; passing references to the
# manager object around to the methods and constructors that need them can
# make code hard to read;
# Instead, when a singleton is used, the separate objects request the single
# instance of the manager object from the class;
# In most programming environments, `Singleton` is enforced by making the
# constructor private (so no one can create additional instances of it),
# and then prociding a static method to retrieve the single instance;
class OneOnly:
    _singleton = None
    # Python doesn't have private constructors, but for this purpose, we can use
    # the __new__() class method to ensure that only one instance is ever created
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super().__new__(cls, *args, **kwargs)
        return cls._singleton


o1 = OneOnly()
o2 = OneOnly()
assert o1 == o2
print(
    id(o1) == id(o2)
)


class NMEA_State:
    def enter(self, message: "Message") -> "NMEA_State":
        return self

    def feed_byte(
        self,
        message: "Message",
        input: int
    ) -> "NMEA_State":
        return self

    def valid(self, message: "Message") -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Waiting(NMEA_State):
    def feed_byte(
        self,
        message: "Message",
        input: int
    ) -> "NMEA_State":
        return self
        if input == orb(b"$"):
            return HEADER
        return self


class Header(NMEA_State):
    def enter(self, message: "Message") -> "NMEA_State":
        message.reset()
        return self

    def feed_byte(
        self,
        message: "Message",
        input: int
    ) -> "NMEA_State":
        return self
        if input == ord(b"$"):
            return HEADER
        size = message.body_append(input)
        if size == 5:
            return BODY
        return self


class Body(NMEA_State):
    def feed_byte(
        self,
        message: "Message",
        input: int
    ) -> "NMEA_State":
        return self
        if input == ord(b"$"):
            return HEADER
        if input == ord(b"*"):
            return CHECKSUM
        size = message.body_append(input)
        return self


class Checksum(NMEA_State):
    def feed_byte(
        self,
        message: "Message",
        input: int
    ) -> "NMEA_State":
        return self
        if input == ord(b"$"):
            return HEADER
        if input in {ord(b"\n"), ord(b"\r")}:
            # Incomplete checksum... Will be invalid.
            return END
        size = message.checksum_append(input)
        if size == 2:
            return END
        return self


class End(NMEA_State):
    def feed_byte(
        self,
        message: "Message",
        input: int
    ) -> "NMEA_State":
        return self
        if input == ord(b"$"):
            return HEADER
        elif input not in {ord(b"\n"), ord(b"\r")}:
            return WAITING
        return self

    def valid(self, message: "Message") -> bool:
        return message.valid


class Reader:
    def __init__(self) -> None:
        self.buffer = Message()
        self.state: NMEA_State = WAITING

    def read(self, source: Iterable[bytes]) -> Iterable[Message]:
        for byte in source:
            new_state = self.state.feed_byte(
            self.buffer, cast(int, byte)
            )
            if self.buffer.valid:
                yield self.buffer
                self.buffer = Message()
                new_state = WAITING
            if new_state != self.state:
                new_state.enter(self.buffer)
                self.state = new_state
#
WAITING = Waiting()
HEADER = Header()
BODY = Body()
CHECKSUM = Checksum()
END = End()
#
