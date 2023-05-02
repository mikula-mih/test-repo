import threading
import time

# `threading.activeCount()`:
#       This function returns the number of currently active thread objects
#       in the program
# `threading.currentThread()`:
#       This function returns the number of thread objects in the current
#       thread control from the caller
# `threading.enumerate()`:
#       This function returns a list of all of the currently active
#       thread objects in the program

# `run()`: This method is executed when a new thread is initialized and started
# `start()`:
#       This method starts the initialized calling thread object by
#       calling the run() method
# `join()`:
#       This method waits for the calling thread object to terminate
#       before continuing to execute the rest of the program
# `isAlive()`:
#       This method returns a Boolean value, indicating whether the calling
#       thread object is currently executing
# `getName()`:
#       This method returns the name of the calling thread object
# `setName()`:
#       This method sets the name of the calling thread object

class MyThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print('Starting thread %s.' % self.name)
        thread_count_down(self.name, self.delay)
        print('Finished thread %s.' % self.name)


def thread_count_down(name, delay):
    counter = 5

    while counter:
        time.sleep(delay)
        print('Thread %s counting down: %i...' % (name, counter))
        counter -= 1



if __name__ == "__main__":
    thread1 = MyThread('A', 0.5)
    thread2 = MyThread('B', 0.5)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print('Finished.')
