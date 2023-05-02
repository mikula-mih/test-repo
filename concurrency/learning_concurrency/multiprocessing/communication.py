
""" Communication between processes """

""" Pipes:
    Anonymous pipes,
    Named pipes
"""
import os
import multiprocessing

class ChildProcess(multiprocessing.Process):

    def __init__(self, pipein):
        super(ChildProcess, self).__init__()
        self.pipein = pipein

    def run(self):
        print("Attempting to pipein to pipe")
        self.pipein = os.fdopen(self.pipein, 'w')
        self.pipein.write("My Name is Elliot")
        self.pipein.close()

def main():
    pipeout, pipein = os.pipe()

    child = ChildProcess(pipein)
    child.start()
    child.join()

    os.close(pipein)
    pipeout = os.fdopen(pipeout)

    pipeContent = pipeout.read()
    print("Pipe: {}".format(pipeContent))

""" Handling Excepitons """
import multiprocessing
import os, sys
import traceback

class MyProcess(multiprocessing.Process):
    def __init__(self, pipein):
        super(MyProcess, self).__init__()
        self.pipein = pipein

    def run(self):
        try:
            raise Exception("This broke stuff")
        except:
            except_type, except_class, tb = sys.exc_info()

            self.pipein = os.fdopen(self.pipein, 'w')
            self.pipein.write(str(except_type))
            self.pipein.close()

def main():
    pipeout, pipein = os.pipe()

    childProcess = MyProcess(pipein)
    childProcess.start()
    childProcess.join()

    os.close(pipein)
    pipeout = os.fdopen(pipeout)

    pipeContent = pipeout.read()
    print("Exception: {}".format(pipeContent))

""" Multiprocessing managers """
import multiprocessing as mp
import queue

def myProcess(ns):
    # Update values within our namespace
    print(ns.x)
    ns.x = 2

def main():
    manager = mp.Manager()
    ns = manager.Namespace()
    ns.x = 1

    print(ns)
    process = mp.Process(target=myProcess, args=(ns,))
    process.start()
    process.join()
    print(ns)

""" Queues """
# communication mechanism between distinct child processes using
# the queue synchronization primitive
from multiprocessing import Pool
import multiprocessing
import queue
import time


def myTask(queue):
    value = queue.get()
    print("Process {} Popped {} from the shared Queue".format(
        multiprocessing.current_process().pid, value)
    )
    queue.task_done()

def main():
    m = multiprocessing.Manager()
    sharedQueue = m.Queue()
    sharedQueue.put(2)
    sharedQueue.put(3)
    sharedQueue.put(4)

    process1 = multiprocessing.Process(target=myTask, args=(sharedQueue,))
    process1.start()
    process1.join()

    process2 = multiprocessing.Process(target=myTask, args=(sharedQueue,))
    process2.start()
    process2.join()

    process3 = multiprocessing.Process(target=myTask, args=(sharedQueue,))
    process3.start()
    process3.join()



# if __name__ == '__main__':
#     main()
