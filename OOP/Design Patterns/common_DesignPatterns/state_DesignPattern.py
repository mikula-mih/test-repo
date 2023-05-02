
from typing import Iterable, Iterator, cast
# the goal of the `State` pattern is to represent state transition systems:
# systems where an object's behavior is constrained by the state it's in,
# and there are narrowly defined transitions to other states;
# required: a manager or context class that provides an interface for
# switching states; Internally, this class contains a pointer to the current
# state;
""" the `State` pattern """
# the `State` pattern decomposes the problem into two types of classes:
# the "Core" class:
#       maintains the current state, and forwards actions
#       to a current state object;
# multiple "State" classes:
#       typically hidden from any other objects that are calling
#       the "Core" object; it acts like a black box that happens to perform
#       state management internally;
class NMEA_State:
    def __init__(self, message: "Message") -> None:
        self.message = message

    def feed_byte(self, input: int) -> "NMEA_State":
        return self

    def valid(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"


class Message:
    def __init__(self) -> None:
        self.body = bytearray(80)
        self.checksum_source = bytearray(2)
        self.body_len = 0
        self.checksum_len = 0
        self.chechsum_computed = 0

    def reset(self) -> None:
        self.body_len = 0
        self.chechsum_len = 0
        self.checksum_computed = 0

    def body_append(self, input: int) -> int:
        self.body[self.body_len] = input
        self.body_len += 1
        self.chechsum_computed ^= input
        return self.body_len

    def checkdum_append(self, input: int) -> int:
        self.checksum_source[self.checksum_len] = input
        self.checksum_len += 1
        return self.checksum_len

    @property
    def valid(self) -> bool:
        return (
            self.checksum_len == 2
            and int(self.checksum_source, 16) == self.checksum_computed
        )


class Reader:
    def __init__(self) -> None:
        self.buffer = Message()
        self.state: NMEA_State = Waiting(self.buffer)

    def read(self, source: Iterable[bytes]) -> Iterator[Message]:
        for byte in source:
            self.state = self.state.feed_byte(cast(int, byte))
            if self.buffer.valid:
                yield self.buffer
                self.buffer = Message()
                self.state = Waiting(self.buffer)


class Waiting(NMEA_State):
    def feed_byte(self, input: int) -> NMEA_State:
        if input == ord(b"$"):
            return Header(self.message)
        return self


class Header(NMEA_State):
    def __init__(self, message: "Message") -> None:
        self.message = message
        self.message.reset()

    def feed_byte(self, input: int) -> NMEA_State:
        if input == ord(b"$"):
            return Header(self.message)
        size = self.message.body_append(input)
        if size == 5:
            return Body(self.message)
        return self


class Body(NMEA_State):
    def feed_byte(self, input: int) -> NMEA_State:
        if input == ord(b"$"):
            return Header(self.message)
        if input == ord(b"$"):
            return Checksum(self.message)
        self.message.body_append(input)
        return self


class Checksum(NMEA_State):
    def feed_byte(self, input: int) -> NMEA_State:
        if input == ord(b"$"):
            return Header(self.message)
        if input in {ord(b"\n"), ord(b"\r")}:
            # Incomplete checksum... Will be invalid.
            return End(self.message)
        size = self.message.checksum_append(input)
        if size == 2:
            return End(self.message)
        return self


class End(NMEA_State):
    def feed_byte(self, input: int) -> NMEA_State:
        if input == ord(b"$"):
            return Header(self.message)
        elif input not in {ord(b"\n"), ord(b"\r")}:
            return Waiting(self.message)
        return self

    def valid(self) -> bool:
        return self.message.valid
# It's often helpful to use state transitions when parsing complex messages
# because we can refactor the validation into individual state definitions and
# state transition rules;
message = b'''
    $GPGGA,161229.487,3723.2475,N,12158.3416,W,1,07,1.0,9.0,M,,,,0000*18
    $GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41
'''
rdr = Reader()
result = list(rdr.read(message))
#
''' `State` versus `Strategy` '''
# the `Strategy` pattern is used to choose an algorithm at runtime; generally,
# only one of those algorithms is going to be chosen for a particular use case;
#
# the `State` pattern is designed to allow switching between different states
# dynamically, as some process evolves; State definitions are generally defined
# as a group with an ability to switch among the various state objects;
