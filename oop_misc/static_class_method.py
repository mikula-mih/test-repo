

# instance methods or just normal methods: operate on a specific instane of
# a class;
class A:
    def do_something(self, x):
        print(f"do_something({self=}, {x=})")
        self.x = x
        print(self.x)

    @classmethod
    def do_something_class(cls, x):
        print(f"do_something_class({cls=}, {x=})")

    @staticmethod
    def do_something_static(x):
        print(f"do_something_static({x=})")


def main():
    a = A()
    # call an instance method on an instance of a class
    a.do_something(1)

####

class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        if type(self).is_weekend(event.date):
            raise ValueError("no")
        self.events.append(event)

    @staticmethod
    def is_weekend(self, date):
        return date.weekday() > 4 # M T W T F S S

    # refering to the class itself inside method
    @classmethod
    def from_json(cls, filename):
        # c = Calendar()  # hard coding breaks inheritance
        c = cls()
        ...
        return c

class WorkCalendar(Calendar):
    pass


c = Calendar()
c.add_event("party")
today = datetime.date.today()
print(c.is_weekend(today))
print(Calendar.is_weekend(today))

###
from dataclasses import dataclass

@dataclass
class Matrix:
    shape: tuple[int, int]

    @staticmethod
    def can_multiply(a, b):
        n, m = a.shape
        k, l = b.shape
        return m == k

###

class StaticMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func

    def __call__(self, *args, **kwargs):    # New in Python 3.10
        return self.func(*args, **kwargs)

# a normal function would bind to the instance
class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func.__get__(owner, type(owner))


if __name__ == "__main__":
    main()
