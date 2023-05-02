import threading
import random

def task(result=0):
    print("Executing our Task")
    for i in range(10):
        result = result + i
    print("I: {}".format(result))
    print("Task Executed {}".format(threading.current_thread()))

""" Concurrent futures """
from concurrent.futures import ThreadPoolExecutor

""" Executor objects """
def main_executor_object():
    executor = ThreadPoolExecutor(max_workers=3)
    task1 = executor.submit(task)
    task1 = executor.submit(task)

""" Context manager """
def main_context_manager():
    print("Starting ThreadPoolExecutor")
    with ThreadPoolExecutor(max_workers=3) as executor:
        future = executor.submit(task, (2))
        future = executor.submit(task, (3))
        future = executor.submit(task, (4))
    print("All tasks complete")

""" Maps """
# map(func, *iterables, timeout=None, chunksize=1)
# results = executor.map(multiplyByTwo, values)
# ==
# for value in values:
#   executor.submit(multiplyByTwo, (value))
def main_maps():
    values = [*range(2,9)]

    def multiplyByTwo(n):
        return 2 * n

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(multiplyByTwo, values)

        for result in results:
            print(result)


""" Shutdown of executor objects """
def main_shutdown():
    with ThreadPoolExecutor(max_workers=2) as executor:
        task1 = executor.submit(task, (1))
        task2 = executor.submit(task, (2))
        executor.shutdown(wait=True)
        task3 = executor.submit(task, (3))
        task4 = executor.submit(task, (4))

if __name__ == '__main__':
    main_executor_object()
    main_context_manager()
    main_maps()
    main_shutdown()
