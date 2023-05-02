
"""
Standard data structures:
    Sets
"""
# implementing thread safety
class LockedSet(set):
    """A set where add(), remove(), and 'in' operator are thread-safe"""

    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(LockedSet, self).__init__(*args, **kwargs)

    def add(self, elem):
        with self._lock:
            super(LockedSet, self).add(elem)

    def remove(self, elem):
        with self._lock:
            super(LockedSet, self).remove(elem)

    def __contains__(self, elem):
        with self._lock:
            super(LockedSet, self).__contains__(elem)

""" Decorators """
# turn the potentially erroneous critical sections of our code into thread-safe
# sections, which can be called without having to worry about race conditions;

def lock(method):

    def newmethod(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    return newmethod


class DecoratorLockedSet(set):
    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(DecoratorLockedSet, self).__init__(*args, **kwargs)

    @locked_method
    def add(self, *args, **kwargs):
        return super(DecoratorLockedSet, self).add(elem)

    @locked_method
    def remove(self, *args, **kwargs):
        return super(DecoratorLockedSet, self).remove(elem)


""" Class decorator """
#
from threading import Lock

def lock_class(methodnames, lockfactory):
    return lambda cls: make_threadsafe(cls, methodnames, lockfactory)

def lock_method(method):
    if getattr(method, '__is_locked', False):
        raise TypeError("Method %r is already locked!" %method)

    def locked_method(self, *arg, **kwarg):
        with self._lock:
            return method(self, *arg, **kwarg)
        locked_method.__name__ = '%s(%s)' % ('lock_method', method.__name__)
        locked_method.__is_locked = True

    return locked_method

def make_threadsafe(cls, methodnames, lockfactory):
    init = cls.__init__
    def newinit(self, *arg, **kwarg):
        init(self, *arg, **kwarg)
        self._lock = lockfacroty()
        cls.__init__ = newinit
        for methodname in methodnames:
            oldmethod = getattr(cls, methodname)
            newmethod = lock_method(oldmethod)
            setattr(cls, mathodname, newmethod)
        return cls

@lock_class(['add', 'remove'], Lock)
class ClassDecoratorLockedSet(set):
    @lock_method # if you double-lock a method, a TypeError is raised
    def lockedMethod(self):
        print("This section of our code would be thread safe")



""" FIFO-based Queues """
#
import threading
import queue
import random
import time

def mySubscriber(queue):
    while not queue.empty():
        item = queue.get()
        if item is None:
            break
        print("{} removed {} from the queue".format(threading.current_thread(), item))
        queue.task_done()
        time.sleep(1)

myQueue = queue.Queue()
for i in range(10):
    myQueue.put(i)

print("Queue Populated")

threads = []
for i in range(4):
    thread = threading.Thread(target=mySubscriber, args=(myQueue,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()


""" LIFO-based Queues """
#
import threading
import queue
import random
import time

def mySubscriber(queue):
    while not queue.empty():
        item = queue.get()
        if item is None:
            break
        print("{} removed {} from the queue".format(threading.current_thread(), item))
        queue.task_done()
        time.sleep(1)

myQueue = queue.LifoQueue()
for i in range(10):
    myQueue.put(i)

print("Queue Populated")

threads = []
for i in range(2):
    thread = threading.Thread(target=mySubscriber, args=(myQueue,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Queue is empty")

""" PriorityQueue """
#
def mySubscriber(queue):
    while not queue.empty():
        item = queue.get()
        if item is None:
            break
        print("{} removed {} from the queue".format(threading.current_thread(), item))
        queue.task_done()
        time.sleep(1)

myQueue = queue.PriorityQueue()

for i in range(5):
    myQueue.put(i, i)

for i in range(5):
    myQueue.put(i, i)

print("Queue Populated")
threads = []
for i in range(2):
    thread = theading.Thread(target=mySubscriber, args=(myQueue,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("Queue is empty")
