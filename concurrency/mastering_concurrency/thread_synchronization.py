import threading
import time

# there are sequential portions and concurrent portions of the code;
# furthermore, even inside of a concurrent portion, some form of coordination
# between different threads/processes is also required
#
# `Thread/process synchronization` is a concept in computer science that
# specifies various mechanisms to ensure that no more than one concurrent
# thread/process can process and execute a particular program portion at a time;
# this portion is known as the `critical section`
#
# The typical goal of thread synchronization is to avoid any potential data
# discrepancies when multiple threads access their shared resources;
# allowing only one thread to execute the critical section of the program at
# a time guarantees that no data conflicts occur in multithreaded applications

"""
`threading.Lock` class
"""

# `threading.Lock()`:
#       This method initializes and returns a new lock object
# `acquire(blocking)`:
#       When this method is called, all of the threads will run synchronously
#       (that is, only one thread can execute the critical section at a time):
#       The optional argument blocking allows us to specify whether the
#       current thread should wait to acquire the lock
#       When `blocking = 0`, the current thread does not wait for the lock
#       and simply returns 0 if the lock cannot be acquired by the thread,
#       or 1 otherwise
#       When `blocking = 1`, the current thread blocks and waits for the lock
#       to be released and acquires it afterwards
# `release()`:
#       When this method is called, the lock is released

class MyThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print('Starting thread %s.' % self.name)
        thread_lock.acquire()
        thread_count_down(self.name, self.delay)
        thread_lock.release()
        print('Finished thread %s.' % self.name)


def thread_count_down(name, delay):
    counter = 5

    while counter:
        time.sleep(delay)
        print('Thread %s counting down: %i...' % (name, counter))
        counter -= 1


thread_lock = threading.Lock()

thread1 = MyThread('A', 0.5)
thread2 = MyThread('B', 0.5)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('Finished.')
