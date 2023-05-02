import threading
import time
import random

""" Locks """
counter = 1
lock = threading.Lock()

def workerA_no_lock():
    global counter
    while counter < 10:
        counter += 1
        print("Worker A is incrementing counter to {}".format(counter))
        sleepTime = random.randint(0, 1)
        time.sleep(sleepTime)

def workerB_no_lock():
    global counter
    while counter > - 10:
        counter -= 1
        print("Worker B is decrementing counter to {}".format(counter))
        sleepTime = random.randint(0, 1)
        time.sleep(sleepTime)

def workerA_lock():
    global counter
    lock.acquire()
    try:
        while counter < 1000:
            counter += 1
            print("Worker A is incrementing counter to {}".format(counter))
            sleepTime = random.randint(0, 1)
            time.sleep(sleepTime)
    finally:
        lock.release()

def workerB_lock():
    global counter
    lock.acquire()
    try:
        while counter > - 1000:
            counter -= 1
            print("Worker B is decrementing counter to {}".format(counter))
            sleepTime = random.randint(0, 1)
            time.sleep(sleepTime)
    finally:
        lock.release()

def main(workerA, workerB):
    t0 = time.time()
    thread1 = threading.Thread(target=workerA)
    thread2 = threading.Thread(target=workerB)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    t1 = time.time()
    print("Execution Time {}".format(t1 - t0))

""" RLocks """
# Reentrant-locks | RLocks

class myWorker():
    def __init__(self):
        self.a = 1
        self.b = 2
        self.Rlock = threading.RLock()

    def modifyA(self):
        with self.Rlock:
            print("Modifying A : RLock Acquired: {}".format(self.Rlock._is_owned()))
            print("{}".format(self.Rlock))
            self.a = self.a + 1
            time.sleep(5)

    def modifyB(self):
        with self.Rlock:
            print("Modifying B : RLock Acquired: {}".format(self.Rlock._is_owned()))
            print("{}".format(self.Rlock))
            self.b = self.b + 1
            time.sleep(5)

    def modifyBoth(self):
        with self.Rlock:
            print("Rlock acquired, modifying A and B")
            print("{}".format(self.Rlock))
            self.modifyA()
            self.modifyB()
        print("{}".format(self.Rlock))

""" Condition """
# A condition is a synchronization primitve that waits on a signal from another
# thread;

class Publisher(threading.Thread):
    def __init__(self, integers, condition):
        self.condition = condition
        self.integers = integers
        threading.Thread.__init__(self)

    def run(self):
        while True:
            integer = random.randint(0, 1000)
            self.condition.acquire()
            print("Condition Acquired by Publisher: {}".format(self.name))
            self.integers.append(integer)
            self.condition.notify()
            print("Condition Released by Publisher: {}".format(self.name))
            self.condition.release()
            time.sleep(1)

class Subscriber(threading.Thread):
    def __init__(self, integers, condition):
        self.condition = condition
        self.integers = integers
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.condition.acquire()
            print("Condition Acquired by Consumer: {}".format(self.name))
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print("{} Popped from list by Consumer: {}".format(integer, self.name))
                    break
                print("Condition Wait by {}".format(self.name))
                self.condition.wait()
            print("Consumer {} Releasing Condition".format(self.name))
            self.condition.release()

def Pub_Sub():
    integers = []
    condition = threading.Condition()
    # our Publisher
    pub1 = Publisher(integers, condition)
    pub1.start()
    # our Subscribers
    sub1 = Subscriber(integers, condition)
    sub1 = Subscriber(integers, condition)
    sub1.start()
    sub2.start()
    # Joining our Threads
    pub1.join()
    consumer1.join()
    consumer2.join()

if __name__ == '__main__':
    # main(workerA_no_lock, workerB_no_lock)
    # main(workerA_lock, workerB_lock)
    #
    # workerA = myWorker()
    # workerA.modifyBoth()
    #
    Pub_Sub()
