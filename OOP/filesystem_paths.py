
""" Filesystem paths """
# most operating systems provide a `filesystem`, a way of mapping a logical
# abstraction of directories (often depicted as folders) and files to the bits
# and bytes stored on a hard drive or another storage device;
import os.path
# inside the `os` module is the `os.path` module;
# an `os.sep` aattribute representing the path separator; that's a "/" on POSIX-
# compliant OSes and "\" for Windows;
path = os.path.abspath(
    os.sep.join(
        ["", "Users", "dusty", "subdir", "subsubdir", "file.ext"]))
print(path)
# the `os.path` module conceals some of the platform-specific details;
from pathlib import Path
# the Python language designers included a module called `pathlib` in the standard
# library; it's an object-oriented representation of paths and files that is much
# more pleasant to work with;
path = Path("/Users") / "dusty" / "subdir" / "subsubdir" / "file.ext"
print(path)
# this is an elegant use of overloading Python's `__truediv__()` method to provide
# this feature for `Path` object;
from typing import Callable

def scan_python_1(path: Path) -> int:
    sloc = 0
    with path.open() as source:
        for line in source:
            line = line.strip()
            if line and not line.startswith("#"):
                sloc += 1
    return sloc

def count_sloc(path: Path, scanner: Callable[[Path], int]) -> int:
    if path.name.startswith("."):
        return 0
    elif path.is_file():
        if path.suffix != ".py":
            return 0
        with path.open() as source:
            return scanner(path)
    elif path.is_dir():
        count = sum(
            count_sloc(name, scanner) for name in path.iterdir())
        return count
    else:
        return 0
# the `current working directory (CWD)`
base = Path.cwd().parent
chapter = base / "ch_02"
count = count_sloc(chapter, scan_python_1)
print(f"{chapter.relative_to(base)}: {count} lines of code")
# a few more methods and attributes of a `Path` object:
# `.absolute()` returns the full path from the root of the filesystem;
# `.patent` returns a path to the parent directory;
# `.exists()` checks whether the file or directory exists;
# `.mkdir()` creates a directory at the current path; it takes Boolean `parents`
# and `exist_ok` arguments to indicate that it should recursively create the
# directories if necessary and that it shouldn't raise an exception if the
# directory already exists;
zipfile.ZipFile(Path('nothing.zip'), 'w').writestr('filename', 'contents')
# almost all of the standard library modules that accept a string path can also
# accept a `pathlib.Path` object; an `os.PathLike` type hint is used to describe
# parameters that accept a `Path`;

""" Serializing object """
# persistent objects;
# `serializing` and `deserializing`
# service described as `RESTful` concept is `REpresentational State Transfer`;
import pickle
# the Python `pickle` module is an object-oriented way to store object state
# directly in a special storage format;
with open('pickled_list', 'wb') as file:
    pickle.dump(some_data, file)
with open("pickled_list", 'rb') as file:
    loaded_data = pickle.load(file)

assert loaded_data == some_data
# Customizing pickles
from threading import Timer
import datetime
from urllib.request import urlopen

class URLPolling;
    def __init__(self, url: str) -> None:
        self.url = url
        self.contents = ""
        self.last_updated: datetime.datetime
        self.timer: Timer
        self.update()

    def update(self) -> None:
        self.contents = urlopen(self.url).read()
        self.last_updated = datetime.datetime.now()
        self.schedule()

    def schedule(self) -> None:
        self.timer = Timer(3600, self.update)
        self.timer.setDaemon(True)
        self.timer.start()
# objects like `url`, `contents`, and `last_updated` are all picklable, but if we
# try to pickle an instance of this class, things go a little nutty;
poll = URLPolling("http://dusty.phillips.codes")
pickle.dumps(poll)  # returns an ERROR
# When pickle tries to serialize an object, it simply tries to store the state, the value
# of the object's __dict__ attribute; __dict__ is a dictionary mapping all the attribute
# names on the object to their values. Luckily, before checking __dict__, pickle checks
# to see whether a __getstate__() method exists. If it does, it will store the return
# value of that method instead of the __dict__ object.
    def __getstate__(self) -> dict[str, Any]:
        pickleable_state = self.__dict__.copy()
        if "timer" in pickleable_state:
            del pickleable_state["timer"]
        return pickleable_state

    def __setstate__(self, pickleable_state: dict[str, Any]) -> None:
        self.__dict__ = pickleable_state
        self.schedule()
#
# Serializing objects using JSON
import json
"""
Extensible Markup Language (XML)
Yet Another Markup Language (YAML)
Comma-Separated Value (CSV)
JavaScript Object Notation (JSON)
"""
class Contact:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return("{} {}".format(self.first, self.last))

c = Contact("Noriko", "Hannah")
json.dumps(c.__dict__)

class ContactEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Contact):
            return {
                "__class__": "Contact",
                "first": obj.first,
                "last": obj.last,
                "full_name": obj.full_name,
            }
        return super().default(obj)
#
c = Contact("Noriko", "Hannah")
text = json.dumps(c, cls=ContactEncoder)

    def decode_contact(json_object: Any) -> Any:
        if json_object.get("__class__") == "Contact":
            return COntact(json_object["first"], json_object["last"])
        else:
            return json_object
#
some_text = (
    '{"__class__": "Contact", "first": "Milli", "last": "Dale", '
    '"full_name": "Milli Dale"}'
)
c2 = json.loads(some_text, object_hook=decode_contact)
c2.full_name
#








#
