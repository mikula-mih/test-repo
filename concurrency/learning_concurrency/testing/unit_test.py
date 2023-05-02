import unittest
'''
def simpleFunction(x):
    return x + 1

class SimpleFunctionTest(unittest.TestCase):

    def setUp(self):
        print("This is run before all of our tests have a chance to execute")

    def tearDown(self):
        print("This is executed after all of our tests have completed")

    def test_simple_function(self):
        print("Testing that our function works with positive tests")
        self.assertEqual(simpleFunction(2), 3)
        self.assertEqual(simpleFunction(2424614623464623462346), 2424614623464623462347)
        self.assertEqual(simpleFunction(0), 1)


if __name__ == '__main__':
    unittest.main()
'''

from timer import Timer
from urllib.request import Request, urlopen
import ssl

def myFunction():
    myssl = ssl.create_default_context()
    myssl.check_hostname=False
    myssl.verify_mode=ssl.CERT_NONE
    with Timer as t:
        import pdb; pdb.set_trace()
        req = Request('https://tutorialedge.net', headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req, context=myssl)

    print("Elapsed Time: {} seconds".format(t.elapsed_secs))

myFunction()

""" Catching exceptions in child threads """

import sys
import threading
import time
import queue

def myThread(queue):
    while True:
        try:
            time.sleep(2)
            raise Exception("Exception Thrown In Child Thread {}".format(threading.current_thread()))
        except:
            queue.put(sys.exc_info())

queue = queue.Queue()
myThread = threading.Thread(target=myThread, args=(queue,))
myThread.start()

while True:
    try:
        exception = queue.get()
    except Queue.Empty():
        pass
    else:
        print(exception)
        break


""" Benchmarking """
# Micro Benchmarking
import timeit
import time
import random

def func1():
    print("Function 1 Executing")
    time.sleep(3)
    print("Function 2 complete")

def func2():
    print("Function 2 Executing")
    time.sleep(2)
    print("Function 2 complete")

def timeit_benchmark_1():
    start_time = timeit.default_timer()
    func1()
    print(timeit.default_timer() - start_time)

    start_time = timeit.default_timer()
    func2()
    print(timeit.default_timer() - start_time)

def timeit_benchmark_2():
    t1 = timeit.Timer("func1()", setup="from __main__ import func1")
    times = t1.repeat(repeat=2, number=1)
    for t in times:
        print("{} Seconds: ".format(t))

    t2 = timeit.Timer("func2()", setup="from __main__ import func2")
    times = t2.repeat(repeat=2, number=1)
    for t in times:
        print("{} Seconds: ".format(t))

""" Using Decorators """
def timethis(func):

    def function_timer(*args, **kwargs):
        start_time = timeit.default_timer()
        value = func(*args, **kwargs)
        runtime = timeit.default_timer() - start_time
        print("Function {} took {} seconds to run".format(func.__name__, runtime))

        return value

    return function_timer

@timethis
def long_runner():
    for x in range(3):
        sleep_time = random.choice(range(1, 3))
        time.sleep(sleep_time)

long_runner()

""" Timing context manager """
from timeit import default_timer, Timer
from urllib.request import Request, urlopen
import ssl

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.timer = default_timer

    def __enter__(self):
        self.start = default_timer()
        return self

    def __exit__(self, *args):
        end = default_timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000 # millisecs
        if self.verbose:
            print('elapsed time: %f ms' % self.elapsed)

def myFunction():
    # create this context so that we can crawl https sites
    myssl = ssl.create_default_context()
    myssl.check_hostname=False
    myssl.verify_mode=ssl.CERT_NONE
    with Timer() as t:
        req = Request('https://tutorialedge.net', headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req, context=myssl)
        print("Elapsed Time: {} seconds".format(t.elapsed))
