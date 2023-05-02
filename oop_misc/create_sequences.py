
""" Indexes and slices """
# `slice` is a built-in object in Python
interval = slice(1, 7, 2)
my_nymbers[interval]
interval = slice(None, 3)
my_numbers[interval] == my_numbers[:3] # True

# `__getitem__` - this magic method is called, when smth like myobject[key] is
# called, passing the key as a parameter;

# `sequence` is an object that implements both __getitem__ and __len__, and
# for this reason, it can be iterated over;

# use of encapsulation;
# another way of doing it is through inheritance, in which case we extend the
# `collections.UserList` base class;

class Items:
    def __init__(self, *values):
        self._values = list(values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item):
        return self.values.__getitem__(item)

# >>> range(1, 100)[25:50]
# range(26, 51)


""" Contex Manager """

def stop_database():
    run("systemctl stop postgresql.service")

def start_database():
    run("systemctl start postgresql.service")

class DBHandler:
    def __enter__(self):
        stop_database()
        return self

    def __exit__(self, exc_type, ex_value, ex_traceback):
        start_database()

def db_backup():
    run("pg_dump database")

def main():
    with DBHandler():
        db_backup()

# the contextmanager generator
import contextlib

@contextlib.contextmanager
def db_handler():
    stop_database()
    yield
    start_database()

with db_handler():
    db_backup()

# contextmanager decorator
class dbhandler_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        stop_database()

    def __exit__(self, ext_type, ex_value, ex_traceback):
        start_database()

@dbhandler_decorator()
def offline_backup():
    run("pg_dump database")

#
""" Iterable objects """
from datetime import timedelta

class DateRangeIterable:
    """An iterable that contains its own iterator object."""

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today


for day in DateRangeIterable(date(2018, 1, 1), date(2018, 1, 5)):
    print(day)

r = DateRangeIterable(date(2018, 1, 1), date(2018, 1, 5))
next(r)
next(r)
next(r)

r1 = DateRangeIterable(date(2018, 1, 1), date(2018, 1, 5))
print(
    ", ".join(map(str, r1))
)
# The difference is that each for loop is calling __iter__ again,
# and each one of those is creating the generator again;
#This is called a `container iterable`
# In general, it is a good idea to work with container iterables when dealing
# with generators;
class DateRangeContainerIterable:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __iter__(self):
        current_day = self.start_date
        while current_day < self.end_date:
            yield current_day
            current_day += timedelta(days=1)

r1 = DateRangeContainerIterable(date(2018, 1, 1), date(2018, 1, 5))
print(
    ", ".join(map(str, r1))
)
print(
    max(r1)
)

""" Creating sequences """
# A `sequence` is an object that implements __len__ and __getitem__
# and expects to be able to get the elements it contains, one at a time,
# in order, starting at zero as the first index;
#
# The implementation with an iterable will use less memory,
# but it takes up to O(n) to get an element,
# whereas implementing a sequence will use more memory (because we have to
# hold everything at once), but supports indexing in constant time, O(1)
class DateRangeSequence:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._range = self._create_range()

    def _create_range(self):
        days = []
        current_day = self.start_date
        while current_day < self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days

    def __getitem__(self, day_no):
        return self._range[day_no]

    def __len__(self):
        return len(self._range)

s1 = DateRangeSequence(date(2018, 1, 1), date(2018, 1, 5))
for day in s1:
    print(day)
print(s1[0])

""" Container objects """
# Containers are objects that implement a __contains__ method
# (that usually returns a Boolean value).
# This method is called in the presence of the in keyword of Python.
class Boundaries:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __contains__(self, coord):
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.limits = Boundaries(width, height)

    def __contains__(self, coord):
        return coord in self.limits

def mark_coordinate(grid, coord):
    if coord in grid:
        grid[coord] = MARKED

""" Dynamic attributes for objects """
# the __getattr__ method
class DynamicAttributes:
    def __init__(self, attribute):
        self.attribute = attribute

    def __getattr__(self, attr):
        if attr.startswith("fallback_"):
            name = attr.replace("fallback_", "")
            return f"[fallback resolved] {name}"
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute {attr}"
    )

dyn = DynamicAttributes("value")
print(dyn.attribute)
print(dyn.fallback_test) # '[fallback resolved] test'
dyn.__dict__["fallback_new"] = "new value"
print(dyn.fallback_new)
print(getattr(dyn, "something", "default"))
# Be careful when implementing a method so dynamic as __getattr__,
# and use it with caution. When implementing __getattr__, raise AttributeError;

""" Callable objects """
# The magic method __call__ will be called when we try to execute our object
# as if it were a regular function;
#
# When we have an object, a statement like this object(*args, **kwargs)
# is translated in Python to object.__call__(*args, **kwargs)
from collections import defaultdict

class CallCount:
    def __init__(self):
        self._counts = defaultdict(int)

    def __call__(self, argument):
        self._counts[argument] += 1
        return self._counts[argument]

cc = CallCount()
cc(1) # 1
cc(2) # 1
cc(1) # 2
cc(1) # 3
cc("something") # 1
#
""" Mutable default arguments """
# don't use mutable objects as the default arguments of functions
def wrong_user_display(user_metadata: dict = {"name": "John", "age": 30}):
    name = user_metadata.pop("name")
    age = user_metadata.pop("age")
    return f"{name} ({age})"

wrong_user_display()
# 'John (30)'
wrong_user_display({"name": "Jane", "age": 25})
# 'Jane (25)'
wrong_user_display()
# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# File ... in wrong_user_display
# name = user_metadata.pop("name")
# KeyError: 'name'
#
def user_display(user_metadata: dict = None):
    user_metadata = user_metadata or {"name": "John", "age": 30}

    name = user_metadata.pop("name")
    age = user_metadata.pop("age")

    return f"{name} ({age})"

""" Extending built-in types """
#
class BadList(list):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        if index % 2 == 0:
            prefix = "even"
        else:
            prefix = "odd"
        return f"[{prefix}] {value}"

bl = BadList((0, 1, 2, 3, 4, 5))
print(bl[0])
print(".join(bl))
# TypeError: sequence item 0: expected str instance, int found
#
from collections import UserList

class GoodList(UserList):
    def __getitem__(self, index):
        value = super().__getitem__(index)
        if index % 2 == 0:
            prefix = "event"
        else:
            prefix = "odd"
        return f"[{prefix}] {value}"

g1 = GoodList((0, 1, 2))
print(g1[0])
print("; ".join(g1))
# Don't extend directly from dict, use collections.UserDict instead.
# For lists, use collections.UserList,
# and for strings, use collections.UserString;
