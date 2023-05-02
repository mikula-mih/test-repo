from __future__ import annotations
# `Concurrency` is the art  of making a computer do (or appear to do) multiple
# things at once; In modern systems, it can also literally mean doing two or
# more things simultaneously on separate processor cores;
""" Concurrency processing """
# Concurrent work requires some method for synchronizing access to shared resources;
# One essential power of large, modern computers is managing concurrency through
# operating system features, collectively called the kernel;
#
# 1. the operating system runs > 1 program at a time:
#   `subprocess` & `multiprocessing` modules:
#   each program is carefully sequestered from all other programs;
# 2. allow a single program to have multiple concurrent threads of operation:
#   `threading` module:
#   gives access to multi-threading; each thread has complete access to the
#   data in all other threads;
#
# Additionally, `concurrent.futures` & `asyncio` provide easier-to-use wrappers
# around the underlying libraries;
#
''' `Threads` '''
# a `Thread` is a sequence of Python byte-code instructions that may be
# interrupted and resumed; the idea is to create separate, concurrent threads to
# allow computation to proceed while the program is waiting for I/O to happen;
import math
import random
from threading import Thread, Lock
import time

THE_ORDERS = [
    "Reuben",
    "Ham and Cheese",
    "Monte Cristo",
    "Tuna Melt",
    "Cuban",
    "Grilled Cheese",
    "French Dip",
    "BLT",
]

class Chef(Thread):
    def __init__(self,  name: str) -> None:
        super().__init__(name=name)
        self.total = 0

    def get_order(self) -> None:
        self.order = THE_ORDERS.pop(0)

    def prepare(self) -> None:
        """Simulate doing a lot of work a BIG computaion"""
        start = time.monotonic()
        target = start + 1 + random.random()
        for i in range(1_000_000_000):
            self.total += math.factorial(i)
            if time.monotonic() >= target:
                break
        print(
            f"{time.monotonic():.3f} {self.name} made {self.order}")

    def run(self) -> None:
        while True:
            try:
                self.get_order()
                self.prepare()
            except IndexError:
                break   # No more orders
#
Mo = Chef("Micheal")
Constantine = Chef("Constantine")
# to synchronize access to any code that reads or (especially) writes a shared
# variable; Python's `threading` library offers the `Lock` class, which can be
# used via the `with` statement to create a context where a single thread has
# access to update shared objects;
#
# Multiprocessing
from multiprocessing import Process, cpu_count
import os

class MuchCPU(Process):
    def run(self) -> None:
        print(f"OS PID {os.getpid()}")

        s = sum(
            2*i+1 for i in range(100_000_000)
        )
#
if __name__ == "__main__":
    choice = input("Threading or Multiprocessing [t/m]: ")
    if choice == 't':
        random.seed(42)
        Mo.start()
        Constantine.start()
    else:
        # implement a subclass `Process` (instead of `Thread`)
        workers = [MuchCPU() for f in range(cpu_count())]
        t = time.perf_counter()
        for p in workers:
            p.start()
        for p in workers:
            p.join()
        print(f"work took {time.perf_counter() - t:.3f} seconds")
#
# Usually, it is safest to force communication between threads to happen using
# a lightweight data structure that already uses locks appropriately.
# Python offers the `queue.Queue` class to do this; a number of threads can write
# to a queue, where a single thread consumes the results. This gives us a tidy,
# reusable, proven technique for having multiple threads sharing
# a data structure. The `multiprocessing.Queue` class is nearly identical;
#
# However, this advantage is usually nullified by the fact that, in Python,
# it is impossible for two threads running on different CPU cores to be
# performing calculations at exactly the same time.
#
# the global interpreter lock
# In order to efficiently manage memory, garbage collection, and calls to
# machine code in native libraries, Python has a `global interpreter lock`, or
# `GIL`. It's impossible to turn off, and it means that thread scheduling is
# constrained by the GIL preventing any two threads from doing computations at
# the exact same time; the work is interleaved artificially.
#
# When confronted with a compute-intensive algorithm, it may help to switch to
# using the `dask` package to manage the processing;
#
# `ThreadPool` feature
#
# Multiprocessing
# Threads exist within a single OS process; that's why they can share access
# to common objects. We can do concurrent computing at the process level, also.
# Unlike threads, separate processes cannot directly access variables set up by
# other processes. This independence is helpful because each process has its own
# GIL and its own private pool of resources. On a modern multi-core processor,
# a process may have its own core, permitting concurrent work with other cores.
#
# The multiprocessing library is designed for when CPU-intensive jobs need to
# happen in parallel and multiple cores are available. Multiprocessing is not as
# useful when the processes spend a majority of their time waiting on I/O
# (for example, network, disk, database, or keyboard), but it is the way to go
# for parallel computation.
#
# The multiprocessing module spins up new operating system processes to do the
# work. This means there is an entirely separate copy of the Python interpreter
# running for each process.
#





#
