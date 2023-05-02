from __future__ import annotations

""" Unit Testing """
def average(data: list[Optional[int]]) -> float:
    """
    GIVEN a list, data = [1, 2, None, 3, 4]
    WHEN we compute m = average(data)
    THEN the result, m, is 2.5
    """
    pass
# Python's built-in test library;
import unittest
# this library provides a common object-oriented interface for `unit tests`;
# the `TestCase` class
class CheckNumbers(unittest.TestCase):
    def test_int_float(self) -> None:
        self.assertEqual(1, 1.0)

    def test_str_float(self) -> None:
        self.assertEqual(1, "1")

if __name__ == '__main__':
    unittest.main()

""" pytest """
# Unit testing with `pytest`:
# >>> python -m pip install pytest
#
# When we run `pytest`, it starts in the current folder and searches for any modules
# or sub packages with names beginning with the characters `test_`. (Including the
# `_` character.) If any functions in this module also start with `test` (no _ required),
# they will be executed as individual tests. Furthermore, if there are any classes
# in the module whose name starts with Test, any methods on that class that start
# with `test_` will also be executed in the test environment.
#
# It also searches in a folder named – unsurprisingly – tests. Because of this, it's
# common to have code broken up into two folders: the src/ directory contains the
# working module, library, or application, while the tests/ directory contains all the
# test cases.
def test_int_float() -> None:
    assert 1 == 1.0
# Classes can be useful for grouping related tests together or for tests that
# need to access related attributes or methods on the class
class TestNumbers:
    def test_int_float(self) -> None:
        assert 1 == 1.0

    def test_int_str(self) -> None:
        assert 1 == "1"

# if we are writing class-based tests, we can use two methods called `setup_method()`
# and `teardown_method()`; they are called before and after each test method in
# the class to perform setup and cleanup duties, respectively;
from typing import Any, Callable

def setup_module(module: Any) -> None:
    print(f"setting up MODULE {module.__name__}")

def teardown_module(module: Any) -> None:
    print(f"tearing down MODULE {module.__name__}")

def test_a_function() -> None:
    print("RUNNING TEST FUNCTION")

class BaseTest:
    @classmethod
    def setup_class(cls: type["BaseTest"]) -> None:
        print(f"setting up CLASS {cls.__name__}")

    @classmethod
    def teardown_class(cls: type["BaseTest"]) -> None:
        print(f"tearing down CLASS {cls.__name__}\n")

    def setup_method(self, method: Callable[[], None]) -> None:
        print(f"setting up METHOD {method.__name__}")

    def teardown_method(self, method: Callable[[], None]) -> None:
        print(f"tearing down METHOD {method.__name__}")

class TestClass1(BaseTest):
    def test_method_1(self) -> None:
        print("RUNNING METHOD 1-1")

    def test_method_2(self) -> None:
        print("RUNNING METHOD 1-2")

class TestClass2(BaseTest):
    def test_method_1(self) -> None:
        print("RUNNING METHOD 2-1")

    def test_method_2(self) -> None:
        print("RUNNING METHOD 2-2")
# >>> python -m pytest --capture=no <test_setup_teardown>.py
""" pytest fixtures for setup and teardown """
# `fixtures` are functions to build the GIVEN condition, prior to a test's WHEN step;
from typing import List, Optional

class StatsList(List[Optional[float]]):
    """Stats with None objects rejected"""

    def mean(self) -> float:
        clean = list(filter(None, self))
        return sum(clean) / len(clean)

    def median(self) -> float:
        clean = list(filter(None, self))
        if len(clean) % 2:
            return clean[len(clean) // 2]
        else:
            idx = len(clean) // 2
            return (clean[idx] + clean[idx - 1]) / 2

    def mode(self) -> list[float]:
        freqs: DefaultDict[float, int] = collecitons.defaultdict(int)
        for item in filter(None, self):
            freqs[item] += 1
        mode_freq = max(freqs.values())
        modes = [item
            for item, value in freqs.items()
            if value == mode_freq]
        return modes

import pytest
from stats import StatsList

@pytest.fixture
def valid_stats() -> StatsList:
    return StatsList([1, 2, 2, 3, 3, 4])

def test_mean(valid_stats: StatsList) -> None:
    assert valid_stats.mean() == 2.5

def test_median(valid_stats: StatsList) -> None:
    assert valid_stats.median() == 2.5
    valid_stats.append(4)
    assert valid_stats.median() == 3

def test_mode(valid_stats: StatsList) -> None:
    assert valid_stats.mode() == [2, 3]
    valid_stats.remove(2)
    assert valid_stats.mode() == [3]
#
import tarfile
from pathlib import Path
import hashlib

def checksum(source: Path, checksum_path: Path) -> None:
    if checksum_path.exists():
        backup = checksum_path.with_stem(f"(old) {chechsum_path.stem}")
        backup.write_text(checksum_path.read_text())
    checksum = hashlib.sha256(source.read_bytes())
    checksum_path.write_text(f"{source.name} {checksum.hexdigest()}\n")
#
import checksum_writer
import pytest
from pathlib import Path
from typing import Iterator
import sys

@pytest.fixture
def working_directory(tmp_path: Path) -> Iterator[tuple[Path, Path]]:
    working = tmp_path / "some_directory"
    working.mkdir()
    source = working / "data.txt"
    source.write_bytes(b"Hello, world!\n")
    checksum = working / "checksum.txt"
    checksum.write_txt("data.txt Old_Checksum")

    yield source, checksum

    checksum.unlink()
    source.unlink()
#
@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="requires python3.9 feature")
def test_checksum(working_directory: tuple[Path, Path]) -> None:
    source_path, old_checksum_path = working_directory
    checksum_writer.checksum(source_path, old_checksum_path)
    backup = old_checksum_path.with_stem(
        f"(old) {old_chechsum_path.stem}")
    assert backup.exists()
    assert old_checksum_path.exists()
    name, checksum = old_checksum_path.read_text().rstrip().split()
    assert name == source_path.name
    assert (
        checksum == ""
        ""
    )
#
import json
from pathlib import Path
import socketserver
from typing import TextIO
import pickle
import struct

class LogDataCatcher(socketserver.BaseRequestHandler):
    log_file: TextIO
    count: int = 0
    size_format = ">L"
    size_bytes = struct.calcsize(size_format)

    def handle(self) -> None:
        size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
        while size_header_bytes:
            payload_size = struct.unpack(
                LogDataCatcher.size_format, size_header_bytes)
            payload_bytes = self.request.recv(payload_size[0])
            payload = pickle.loads(payload_bytes)
            LogDataCatcher.count += 1
            self.log_file.write(json.dumps(payload) + "\n")
            try:
                size_header = self.request.recv(
                    LogDataCatcher.size_bytes)
            except (ConnectionResetError, BrokenPipeError):
                break

def main(host: str, port: int, target: Path) -> None:
    with target.open("w") as unified_log:
        with socketserver.TCPServer(
                (host, port), LogDataCatcher) as server:
            server.serve_forever()

if __name__ == "__main__":
    HOST, PORT = "localhost", 18842
    main(HOST, PORT, Path("one.log"))
#
import logging
import logging.handlers
import time
import sys
from math import factorial

logger = logging.getLogger("app")

def work(i: int) -> int:
    logger.info("Factorial %d", i)
    f = factorial(i)
    logger.info("Factorial(%d) = %d", i, f)
    return f

if __name__ == "__main__":
    HOST, PORT = "localhost", 18842
    socket_handler = logginh.handlers.SocketHandler(HOST, PORT)
    stream_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(
        handlers=[socket_handler, stream_handler],
        level=logging.INFO)

    for i in range(10):
        work(i)

    logging.shutdown()
#
import subprocess
import signal
import time
import pytest
import logging
import sys
import remote_logging_app
from typing import Iterator, Any

@pytest.fixture(scope="session")
def log_catcher() -> Iterator[None]:
    print("loading server")
    p = subprocess.Popen(
        ["python3", "src/log_catcher.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(0.25)

    yield

    p.terminate()
    p.write()
    if p.stdout:
        print(p.stdout.read())
    assert (
        p.returncode == -signal.SIGTERM.value
    ), f"Error in watcher, returncode={p.returncode}"

@pytest.fixture
def logging_config() -> Iterator[None]:
    HOST, PORT = "localhost", 18842
    socket_handler = logging.handlers.SocketHandler(HOST, PORT)
    remote_logging_app.logger.addHandler(socket_handler)
    yield
    socket_handler.close()
    remote_logging_app.logger.removeHandler(socket_handler)
#
def test_1(log_catcher: None, logging_config: None) -> None:
    for i in range(10):
        r = remote_logging_app.work(i)
def test_2(log_catcher: None, logging_config: None) -> None:
    for i in range(1, 10):
        r = remote_logging_app.work(52 * i)
#
import sys
import pytest

def test_simple_skip() -> None:
    if sys.platform != "ios":
        pytest.skip("Test works only on Pythonista for ios")
    import location # type: ignore [import]

    img = location.render_map_snapshot(36.8508, -76.2859)
    assert img is not None
#
@pytest.mark.skipif(
    sys.version_info < (3, 9),
    reason="requires 3.9, Path.removeprefix()"
)
def test_feature_python39() -> None:
    file_name = "(old) myfile.dat"
    assert file_name.removeprefix("(old) ") == "myfile.dat"
# we'll often replace all of the interface objects with imitations,
# called "mocks," to isolate the unit being tested

""" Imitating object using `Mocks` """
import datetime
from enum import Enum
import redis

class Status(str, Enum):
    CANCELLED = "CANCELLED"
    DELAYED = "DELAYED"
    ON_TIME = "ON TIME"

class FlightStatusTracker:
    def __init__(self) -> None:
        self.redis = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def change_status(self, flight: str, status: Status) -> None:
        if not isinstance(status, Status):
            raise ValueError(f"{status!r} is not a valid Status")
        key = f"flightno:{flight}"
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        value = f"{now.isoformat()}|{status.value}"
        self.redis.set(key, value)

    def get_status(self, flight: str) -> tuple[datetime.datetime, Status]:
        key = f"flightno:{flight}"
        value = self.redis.get(key).decode("utf-8")
        text_timestamp, text_status = value.split("|")
        timestamp = datetime.datetime.fromisoformat(text_timestamp)
        status = Status(text_status)
        return timestamp, status
#
import datetime
import flight_status_redis
from unittest.mock import Mock, patch, call
import pytest

@pytest.fixture
def mock_redis() -> Mock:
    mock_redis_instance = Mock(set=Mock(return_value=True))
    return mock_redis_instance

@pytest.fixture
def tracker(
    monkeypatch: pytest.MonkeyPatch, mock_redis: Mock
) -> flight_status_redis.FlightStatusTracker:
    fst = flight_status_redis.FlightStatusTracker()
    monkeypatch.setattr(fst, "redis", mock_redis)
    return fst

def test_monkeypatch_class(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    with pytest.raises(ValueError) as ex:
        tracker.change_status("AC101", "lost")
    assert ex.value.args[0] == "'lost' is not a valid Status"
    assert mock_redis.set.call_count == 0
#
def test_patch_class(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)
    utc = datetime.timezone.utc
    with patch("flight_status_redis.datetime") as mock_datetime:
        mock_datetime.datetime = Mock(now=Mock(return_value=fake_now))
        mock_datetime.timezone = Mock(utc=utc)
        tracker.change_status(
        "AC101", flight_status_redis.Status.ON_TIME)
    mock_datetime.datetime.now.assert_called_once_with(tz=utc)
    expected = f"2020-10-26T23:24:25|ON TIME"
    mock_redis.set.assert_called_once_with("flightno:AC101", expected)
#
def __init__(
    self,
    redis_instance: Optional[redis.Connection] = None
) -> None:
    self.redis = (
        redis_instance
        if redis_instance
        else redis.Redis(host="127.0.0.1", port=6379, db=0)
    )
#
""" the `sentinel` object """
#
class FileChecksum:
    def __init__(self, source: Path) -> None:
        self.source = source
        self.checksum = hashlib.sha256(source.read_bytes())
#
from unitest.mock import Mock, sentinel

@pytest.fixture
def mock_hashlib(monkeypatch) -> Mock:
    mocked_hashlib = Mock(sha256=Mock(return_value=sentinel.checksum))
    monkeypatch.setattr(chechsum_writer, "hashlib", mocked_hashlib)
    return mocked_hashlib

def test_file_checksum(mock_hashlib, tmp_path) -> None:
    source_file = tmp_path / "some_file"
    source_file.write_text("")
    cw = checksum_writer.FileChecksum(source_file)
    assert cw.source == source_file
    assert cw.checksum == sentinel.checksum
#
import pytest
from stats import StatsList

@pytest.fixture
def valid_stats() -> StatsList:
    return StatsList([1, 2, 2, 3, 3, 4])

def test_mean(valid_stats: StatsList) -> None:
    assert valid_stats.mean() == 2.5
#
