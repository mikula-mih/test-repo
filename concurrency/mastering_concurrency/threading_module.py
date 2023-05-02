import threading
from math import sqrt

'''
To create and customize a new thread using the threading module,
there are specific steps that need to be followed:
    1. Define a subclass of the `threading.Thread` class in your program
    2. Override the default `__init__(self [,args])` method
        inside of the subclass, in order to add custom arguments for the class
    3. Override the default `run(self [,args])` method
        inside of the subclass, in order to customize the behavior of
        the thread class when a new thread is initialized and started
'''

def is_prime(x) -> None:
    if x < 2:
        print('%i is not a prime number.' % x)

    elif x == 2:
        print('%i is a prime number.' % x)

    elif x % 2 == 0:
        print('%i is not a prime number.' % x)

    else:
        limit = int(sqrt(x)) + 1
        for i in range(3, limit, 2):
            if x % i == 0:
                print('%i is not a prime number.' % x)

    print('%i is a prime number.' % x)

class MyThread(threading.Thread):
    def __init__(self, x):
        threading.Thread.__init__(self)
        self.x = x

    def run(self):
        print('Starting processing %i.' % x)
        is_prime(self.x)


my_input = [2, 193, 323, 1327, 433785907]

threads = []

for x in my_input:
    temp_thread = MyThread(x)
    temp_thread.start()

    threads.append(temp_thread)

for thread in threads:
    thread.join()

print('Finished.')
