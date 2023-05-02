
# Each Flyweight object has no specific state of its own. Any time it needs
# to perform an operation on SpecificState, that state needs to be passed into
# the Flyweight by the calling code as an argument value.
""" the `Flyweight` pattern """
# the `Flyweight` pattern is a memory optimization pattern;
# ensures that object that share a state can use the same memory for their
# shared state;
# Unlike the Singleton design pattern, which only needs to return one instance of
# a class, a Flyweight design may have multiple instances of the Flyweight classes
from typing import Sequence, Iterator, Union, overload

class Buffer(Sequence[int]):
    # create an Adapter for the underlying bytes object
    # to transform it into an object that can have weak references
    def __init__(self, content: bytes) -> None:
        self.content = content

    def __len__(self) -> int:
        return len(self.content)

    def __iter(self) -> Iterator[int]:
        return iter(self.content)

    @overload
    def __getitem__(self, index: int) -> int:
        ...

    @overload
    def __getitem__(self, index: slice) -> bytes:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[int, bytes]:
        return self.content[index]
#
import abc
from typing import Optional

class Point:
    # Memory optimization via Python's __slots__
    __slots__ = ("latitude", "longitude")

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude
    def __repr__(self) -> str:
        return (
            f"Point(latitude={self.latitude}, "
            f"longitude={self.longitude})"
        )

import weakref

class Message(abc.ABC):
    def __init__(self) -> None:
        self.buffer: weakref.ReferenceType[Buffer]
        self.offset: int
        self.end: Optional[int]
        self.commas: list[int]

    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":
        self.buffer = weakref.ref(buffer)
        self.offset = offset
        self.commas = [offset]
        self.end = None
        for index in range(offset, offset + 82):
            if buffer[index] == ord(b","):
                self.commas.append(index)
            elif buffer[index] == ord(b"*"):
                self.commas.append(index)
                self.end = index + 3
                break
        if self.end is None:
            raise GPSError("Incomplete")
        # TODO: confirm checksum.
        return self

    def __getitem__(self, field: int) -> bytes:
        if (not hasattr(self, "buffer")
            or (buffer := self.buffer()) is None):
            raise RuntimeError("Broken reference")
        start, end = self.commas[field] + 1, self.commas[field + 1]
        return buffer[start:end]

    def get_fix(self) -> Point:
        return Point.from_bytes(
            self.latitude(),
            self.lat_n_s(),
            self.longitude(),
            self.lon_e_w()
        )

    @abc.abstractmethod
    def latitude(self) -> bytes:
        ...
    @abc.abstractmethod
    def lat_n_s(self) -> bytes:
        ...
    @abc.abstractmethod
    def longitude(self) -> bytes:
        ...
    @abc.abstractmethod
    def lon_e_w(self) -> bytes:
        ...
#
class GPGLL(Message):
    def latitude(self) -> bytes:
        return self[1]

    def lat_n_s(self) -> bytes:
        return self[2]

    def longitude(self) -> bytes:
        return self[3]

    def lon_e_w(self) -> bytes:
        return self[4]
#
buffer = Buffer(
    b"$GPGLL,3751.65,S,14507.36,E*77"
)

def  message_factory(header: bytes) -> Optional[Message]:
    # TODO: Add functools.lru_cache to save storage and time
    if header == b"GPGGA":
        return GPGGA()
    elif header == b"GPGLL":
        return GPGLL()
    elif header == b"GPRMC":
        return GPRMC()
    else:
        return None
#
flyweight = message_factory(buffer[1:6])
flyweight.from_buffer(buffer, 0)
flyweight.get_fix()
#
