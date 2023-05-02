import time
import random

""" number crunching """


# Sequential prime factorization
def calculatePrimeFactors(n):
    primefac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primefac.append(d)   # supposing you want multiple factors repeated
            n //= d
        d += 1
    if n > 1:
        primefac.append(n)
    return primefac

def main():
    print("starting number crunching")
    t0 = time.time()
    for i in range(10_000):
        rand = random.randint(20_000, 100_000_000)
        print(calculatePrimeFactors(rand))
    t1 = time.time()
    totalTime = t1 - t0
    print("Execution Time: {}".format(totalTime))

# Concurrent prime factorization
from multiprocessing import Process

def executeProc():
    rand = random.randint(20_000, 100_000_000)
    print(calculatePrimeFactors(rand))

def main_concurrent():
    print("starting number crunching")
    t0 = time.time()
    procs = []
    for i in range(10):
        proc = Process(target=executeProc, args=())
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    t1 = time.time()
    totalTime = t1 - t0
    print("Execution Time: {}".format(totalTime))


if __name__ == "__main__":
    # main()
    main_concurrent()
