from typing import List
# Design Patterns:
#  - creational
#       * deal with providing control over creating objects in various ways
#  - structural
#       * explain how to assemble objects and classes into larger structures
#           while keeping those structures flexible and efficient; deal more with
#           how to organize different parts of application: `Bridge`
#  - behavioral
#       * focus on allowing to choose between different algorithms or particular
#           parts of application should communicate: `Startegy`, `Observer`

# `Singleton` allows to have one single instance of a class; you can use it to
# represent things for which you need only one: graphics device manager, logger;
# Python doesn't have access modifiers so you can't make the initializer private

class Singleton(type):
    # metaclass has a list of instances it maintains
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
# Singleton considered an anti-pettern: breaks object-oriented design principles,
# and you do not have control over creation, don't work well in multi-threaded
# applications

class Logger(metaclass=Singleton):
    def log(self, msg):
        print(msg)


logger = Logger()
logger2 = Logger()
print(logger)
print(logger2)
logger.log("Hello")
logger2.log("Hi")
print()
# `Object pool` manages a fixed number of instances; that's not possible with
# python modules;

class PoolManager:
    def __init__(self, pool):
        self.pool = pool
    def __enter__(self):
        self.obj = self.pool.acquire()
        return self.obj
    def __exit__(self, type, value, traceback):
        self.pool.release(self.obj)


class Reusable:
    def test(self):
        print(f"Using object {self}")


class ReusablePool:
    def __init__(self, size):
        self.size = size
        self.free = []
        self.in_use = []
        for _ in range(size):
            self.free.append(Reusable())

    def acquire(self) -> Reusable:
        if len(self.free) <= 0:
            raise Exception("No more objects are available")
        r = self.free[0]
        self.free.remove(r)
        self.in_use.append(r)
        return r

    def release(self, r: Reusable):
        self.in_use.remove(r)
        self.free.append(r)


pool = ReusablePool(2)
r = pool.acquire()
r2 = pool.acquire()
pool.release(r2)
r3 = pool.acquire()
r.test()
r3.test()
pool.release(r3)

with PoolManager(pool) as r:
    r.test()
