import time
import random
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import threading
import timeit
import math
import os

def someTask(n):
    print("Executing Task {}".format(n))
    time.sleep(n)
    print("Task {} Finished Executing".format(n))

values = [2,3,4,5,6,7,8]

def multiplyByTwo(n):
    time.sleep(random.randint(1, 2))
    return 2 * n

def done(n):
    print("Done: {}".format(n))

def main_1():
    with ThreadPoolExecutor(max_workers=2) as executor:
        task1 = executor.submit(someTask, (1))
        task2 = executor.submit(someTask, (2))
        task3 = executor.submit(someTask, (3))
        task4 = executor.submit(someTask, (4))

        print(task3.cancel())

def main_2():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(multiplyByTwo, values)

        for result in results:
            done(result)

def main_as_complete():
    from urllib.request import Request, URLError, urljoin, urlopen
    from concurrent.futures import ThreadPoolExecutor, as_completed

    URLS = [
    'https://www.google.com',
    'https://www.amazon.com',
    ]

    def checkStatus(url):
        print("Attempting to crawl URL: {}".format(url))
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req)
        return response.getcode(), url

    def printStatus(statusCode):
        print("URL Crawled with status code: {}".format(statusCode))

    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = []
        for url in URLS:
            task = executor.submit(checkStatus, (url))
            tasks.append(task)

        for result in as_completed(tasks):
            printStatus(result)

""" Setting callbacks """
def main_setting_callbacks():
    def task(n):
        print("Processing {}".format(n))

    def taskDone(fn):
        if fn.cancelled():
            print("Our {} Future has been cancelled".format(fn.arg))
        elif fn.done():
            print("Our Task has completed")

    print("Starting ThreadPoolExecutor")
    with ThreadPoolExecutor(max_workers=3) as executor:
        future = executor.submit(task, (2))
        future.add_done_callback(taskDone)

    print("All tasks complete")

""" Chaining callbacks """

def main_callback_chaining():
    def isEven(n):
        print("Checking if {} is even".format(n))
        if type(n) != int:
            raise Exception("Value entered is not an integer")
        if n % 2 == 0:
            print("{} is even".format(n))
            return True
        else:
            print("{} is odd".format(n))
            return False

    with ThreadPoolExecutor(max_workers=4) as executor:
        task1 = executor.submit(isEven, (2))
        task2 = executor.submit(isEven, (3))
        task3 = executor.submit(isEven, ('t'))

    for future in as_completed([task1, task2, task3]):
        print("Result of Task: {}".format(future.result()))

""" ProcessPoolExecutor """

def main_processpoolexecutor():

    def task(n=os.getpid()):
        print("Executing our Task on Process {}".format(n))

    executor = ProcessPoolExecutor(max_workers=3)
    task1 = executor.submit(task)
    task2 = executor.submit(task)


    print("Starting ProcessPoolExecutor with statement")
    with ProcessPoolExecutor(max_workers=3) as executor:
        future = executor.submit(task, (2))
        future = executor.submit(task, (3))
        future = executor.submit(task, (4))

    print("All tasks complete")


def main_computationally_bound_problem():
    PRIMES = [
        112272535095293,
        112582705942171,
        112272535095293,
        115280095190773,
        115797848077099,
        1099726899285419
    ]

    def is_prime(n):
        if n % 2 == 0:
            return False

        sqrt_n = int(math.floor(math.sqrt(n)))
        for i in range(3, sqrt_n + 1, 2):
            if n % i == 0:
                return False
        return True

    t1 = timeit.default_timer()
    with ProcessPoolExecutor(max_workers=4) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime %s' % (number, prime))
    print("{} Seconds Needed for ProcessPoolExecutor".format(timeit.default_timer() - t1))

    t2 = timeit.default_timer()
    with ThreadPoolExecutor(max_workers=4) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime %s' % (number, prime))
    print("{} Seconds Needed for ThreadPoolExecutor".format(timeit.default_timer() - t2))

    t3 = timeit.default_timer()
    for number in PRIMES:
        isPrime = is_prime(number)
        print("{} is prime: {}".format(number, isPrime))
    print("{} Seconds needed for single threaded execution".format(timeit.default_timer() - t3))


if __name__ == '__main__':
    # main_1()
    # main_2()
    # main_as_complete()
    # main_setting_callbacks()
    # main_callback_chaining()
    # main_processpoolexecutor()
    main_computationally_bound_problem()
