
''' the `Decorator pattern` '''
# the `Decorator pattern`: allows us to wrap an object that provides core
# functionality with other objects that alter this functionality;
# the interface of the decorated object is identical to that of the core object;
#
# two primaty uses:
# Enhancing the response of a component as it sends data to a second component;
# Supporting multiple optional behaviors;
import contextlib
import random
import socket

def main_1() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, addr = server.accept()
            dice_response(client)
            client.close()
# the port number must be above 1023. Port numbers 1023 and below are reserved
# and require  special OS privileges;
def dice_response(client: socket.socket) -> None:
    request = client.recv(1024)
    try:
        response = dice.dice_roller(request)
    except (ValueError, KeyError) as ex:
        response = repr(ex).encode("utf-8")
    client.send(response)


def dice_roller(request: bytes) -> bytes:
    request_text = request.decode("utf-8")
    numbers = [random.randint(1, 6) for _ in range(6)]
    response = f"{request_text} = {numbers}"
    return response.encode("utf-8")


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 2401))
    count = input("How many rolls: ") or "1"
    pattern = input("Dice pattern nd6[dk+-]a: ") or "d6"
    command = f"Dice {count} {pattern}"
    server.send(command.encode("utf8"))
    response = server.recv(1024)
    print(response.decode("utf-8"))
    server.close()
# logging decorator
class LogSocket:
    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket

    def recv(self, count: int = 0) -> bytes:
        data = self.socket.recv(count)
        print(
            f"Receiving {data!r} from {self.socket.getpeername()[0]}"
        )
        return data

    def send(self, data: bytes) -> None:
        print(f"Sending {data!r} to {self.socket.getpeername()[0]}")
        self.socket.send(data)

    def close(self) -> None:
        self.socket.close()
#
def main_2() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, addr = server.accept()
            logging_socket = cast(socket.socket, LogSocket(client))
            dice_response(logging_socket)
            client.close()
#
Address = Tuple[str, int]

class LogRoller:
    def __init__(
        self,
        dice: Callable[[bytes], bytes],
        remote_addr: Address
    ) -> None:
        self.dice_roller = dice
        self.remote_addr = remote_addr

    def __call__(self, request: bytes) -> bytes:
        print(f"Receiving {request!r} from {self.remote_addr}")
        dice_roller = self.dice_roller
        response = dice_roller(request)
        print(f"Sending {response!r} to {self.remote_addr}")
        return response
#
import gzip
import io

class ZipRoller:
    def __init__(self, dice: Callable[[bytes], bytes]) -> None:
        self.dice_roller = dice

    def __call__(self, request: bytes) -> bytes:
        dice_roller = self.dice_roller
        response = dice_roller(request)
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="w") as zipfile:
            zipfile.write(response)
        return buffer.getvalue()


def dice_response(client: socket.socket) -> None:
    request = client.recv(1024)
    try:
        remote_addr = client.getpeername()
        roller_1 = ZipRoller(dice.dice_roller)
        roller_2 = LogRoller(roller_1, remote_addr=remote_addr)
        response = roller_2(request)
    except (ValueError, KeyError) as ex:
        response = repr(ex).encode("utf-8")
    client.send(response)
#
''' Decorators in Python '''
# we can use `monkey-patching`;
from functools import wraps

def log_args(funciton: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(function)
    def wrapped_function(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result

    return wrapped_function
#
def test1(a: int, b: int, c: int) -> float:
    return sum(range(a, b + 1)) / c

test1 = lob_args(test1)
test1(1, 9, 2)

@log_args
def test1(a: int, b: int, c: int) -> float:
    return sum(range(a, b + 1)) / c
# rather than save all of the parameters and results, we can keep the cache small
# by discarding the `least recently used (LRU)` values;
from math import factorial
from functools import lru_cache

def binom(n: int, k: int) -> int:
    return factorial(n) // (factorial(k) *  factorial(n - k))

print(f"6-card deals: {binom(52, 6):,d}")

@lru_cache(64)
def binom(n: int, k: int) -> int:
    return factorial(n) // (factorial(k) *  factorial(n - k))
#
class NamedLogger:
    def __init__(self, logger_name: str) -> None:
        self.logger = logging.getLOgger(logger_name)

    def __call__(
        self,
        function: Callable[..., Any]
    ) -> Callable[..., Any]:
        @wraps(function)
        def wrapped_function(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = function(*args, **kwargs)
                ms = (time.perf_counter() - start) * 1_000_000
                self.logger.info(
                    f"{function.__name__}, { ìs:.1f}ìs")
                return result
            except Exception as ex:
                ms = (time.perf_counter() - start) * 1_000_000
                self.logger.error(
                    f"{ex}, {function.__name__}, { ìs:.1f}ìs")
                raise

        return wrapped_function
#
@NamedLogger("log4")
def test4(median: float, sample: float) -> float:
    return abs(sample-median)
#
