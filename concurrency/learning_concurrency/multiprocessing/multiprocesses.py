
""" Subclassing processes """
import multiprocessing
import os
import time
from multiprocessing import Pool

class MyProcess(multiprocessing.Process):
    def __init__(self):
        super(MyProcess, self).__init__()
    def run(self):
        print("Child Process PID: {}".format(multiprocessing.current_process().pid))

def main_subclassing():
    print("Main Process PID: {}".format(multiprocessing.current_process().pid))
    myProcess = MyProcess()
    myProcess.start()
    myProcess.join()

    # spinning up multiple processes in quick succession
    processes = []
    for i in range(os.cpu_count()):
        process = MyProcess()
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    # spinning x distinct child processes, where x is the number of CPU cores
    # currently available on your machine
    print(os.cpu_count())


def task(n):
    print(n)

def myTask(n):
    print("Task processed by Process {}".format(os.getpid()))
    time.sleep(n/2)
    return n * 2

def myTask_new(x, y):
    print("Task processed by Process {}".format(os.getpid()))
    return y*2

""" Multiprocessing pools """
def main_multiprocessing_pools():

    def main_pool():
        with Pool(4) as p:
            print(p.map(task, [2,3,4]))
        """ Submitting tasks to a process pool """
        with Pool(4) as p:
            print(p.apply(myTask, (4,)))
            print(p.apply(myTask, (3,)))
            print(p.apply(myTask, (2,)))
            print(p.apply(myTask, (1,)))

        print("apply_async")

        with Pool(4) as p:
            tasks = []

            for i in range(4):
                t = p.apply_async(func=myTask, args=(i,))
                tasks.append(t)

            for t in tasks:
                t.wait()
                print("Result: {}".format(t.get()))

        print("Map")
        with Pool(4) as p:
            print(p.map(myTask, [4,3,2,1]))

        print("Map_async")
        with Pool(4) as p:
            print(p.map_async(myTask, [4,3,2,1]).get())

        print("Imap")
        with Pool(4) as p:
            for iter in p.imap(myTask, [1,3,2,1]):
                print(iter)

        print("Imap_unordered")
        with Pool(4) as p:
            for iter in p.imap_unordered(myTask, [1,3,2,1]):
                print(iter)

        print("Starmap")
        with Pool(4) as p:
            print(p.starmap(myTask_new, [(4,3),(2,1)]))

        print("Starmap_async")
        with Pool(4) as p:
            print(p.starmap_async(myTask_new, [(4,3),(2,1)]).get())

        print("Maxtasksperchild")
        with Pool(processes=1, maxtasksperchild=2) as p:
            print(p.starmap_async(myTask_new, [(4,3),(2,1), (3,2),(5,1)]).get())
            print(p.starmap_async(myTask_new, [(4,3),(2,1), (3,2),(2,3)]).get())


    main_pool()

    """ Submitting tasks to a process pool """
    # Apply

if __name__ == '__main__':
    main_subclassing()
    main_multiprocessing_pools()
