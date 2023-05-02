

"""
Multithreaded priority queue
"""

# `priority queue` - each of the elements in a priority queue, as the
# name suggests, has a priority associated with it; in other words,
# when an element is added to a priority queue, its priority needs to be specified
#
# Elements can be added to the end of the queue; this task is called `enqueue`
# Elements can also be removed from the beginning of the queue;
#this task is called `dequeue`

# `get()`:
#       This method returns the next element of the calling queue object
#       and removes it from the queue object
# `put()`:
#       This method adds a new element to the calling queue object
# `qsize()`:
#       This method returns the number of current elements in
#       the calling queue object (that is, its size)
# `empty()`:
#       This method returns a Boolean, indicating whether
#       the calling queue object is empty
# `full()`:
#       This method returns a Boolean, indicating whether
#       the calling queue object is full

import queue
import threading
import time

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print('Starting thread %s.' % self.name)
        time.sleep(0.5)
        process_queue()
        print('Exiting thread %s.' % self.name)

def process_queue():
    while True:
        try:
            # obtain the next element of the queue object
            # in a non-blocking manner
            x = my_queue.get(block=False)
        except queue.Empty:
            return
        else:
            print_facotrs(x)

        time.sleep(1)

def print_facotrs(x):
    result_string = "Positive factors of %i are: " % x
    for i in range(1, x + 1):
        if x % i == 0:
            result_string += str(i) + ' '
    result_string += '\n' + '_' * 20 + '\n'

    print(result_string)

# setting up variaqbles
input_ = [1, 10, 4, 3]

# filling the queue
my_queue = queue.Queue()

for x in input_:
    my_queue.put(x)

# initializing and starting 3 threads
thread1 = MyThread('A')
thread2 = MyThread('B')
thread3 = MyThread('C')

thread1.start()
thread2.start()
thread3.start()

# joining all 3 threads
thread1.join()
thread2.join()
thread3.join()

print('Done.')
