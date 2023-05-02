
""" Processes in Python """
from math import sqrt
import multiprocessing


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        pname = self.name

        while True:
            temp_task = self.task_queue.get()

            if temp_task is None:
                print('Exiting {}...'.format(pname))
                self.task_queue.task_done()
                break

            print(f'{pname} processing task: {temp_task}')

            answer = temp_task.process()
            self.task_queue.task_done()
            self.result_queue.put(answer)

class Task():

    def __init__(self, x):
        self.x = x

    def process(self):
        if self.x < 2:
            return f'{self.x} is not a prime number.'

        if self.x == 2:
            return f'{self.x} is a prime number.'

        if self.x % 2 == 0:
            return f'{self.x} is not a prime number.'

        limit = int(sqrt(self.x)) + 1
        for i in range(3, limit, 2):
            if self.x % i == 0:
                return f'{self.x} is not a prime number.'

        return f'{self.x} is a prime number.'

    def __str__(self):
        return f'Checking if {self.x} is a prime or not.'

# Interprocess communication
#
# import time
# import os
# class MyWorker():
#     def __init__(self, x):
#         self.x = x
#
#     def process(self):
#         pname = multiprocessing.current_process().name
#         print('Starting process %s for number %i...' % (pname, self.x))
#
# def work(q):
#     worker = q.get()
#     worker.process()

if __name__ == '__main__':
    # my_queue = multiprocessing.Queue()
    # p = multiprocessing.Process(target=work, args=(my_queue,))
    # p.start()
    # my_queue.put(MyWorker(10))
    # my_queue.close()
    # my_queue.join_thread()
    # p.join()
    # print('Done.')
    #
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # spawning consumers with respect to the
    # number cores available in the system
    n_consumers = multiprocessing.cpu_count()
    print(f'Spawning {n_consumers} consumers...')
    consumers = [Consumer(tasks, results) for i in range(n_consumers)]
    for consumer in consumers:
        consumer.start()

    # enqueueing jobs
    my_input = [2, 36, 101, 193, 323, 513, 1327, 100000, 9999999, 433785907]
    for item in my_input:
        tasks.put(Task(item))

    for i in range(n_consumers):
        tasks.put(None)

    tasks.join()

    for i in range(len(my_input)):
        temp_result = results.get()
        print('Result: ', temp_result)

    print('Done.')
