
""" Reduction Operators in Processes """
import multiprocessing

class ReductionConsumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        pname = self.name
        print('Using process {}...'.format(pname))

        while True:
            num1 = self.task_queue.get()

            if num1 is None:
                print('Exiting process {}.'.format(pname))
                self.task_queue.task_done()
                break

            self.task_queue.task_done()
            num2 = self.task_queue.get()
            if num2 is None:
                print(
                    'Reaching the end with process {} and number {}.'.format(
                        pname, num1
                    )
                )
                self.task_queue.task_done()
                self.result_queue.put(num1)
                break

            print('Running process {0} on numbers {1} and {2}'.format(
                pname, num1, num2)
            )
            self.task_queue.task_done()
            self.result_queue.put(num1 + num2)


def reduce_sum(array):
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.JoinableQueue()
    result_size = len(array)

    n_consumers = multiprocessing.cpu_count()

    for item in array:
        results.put(item)

    while result_size > 1:
        tasks = results
        results = multiprocessing.JoinableQueue()

        consumers = [ReductionConsumer(tasks, results)
                        for i in range(n_consumers)]
        for consumer in consumers:
            consumer.start()

        for i in range(n_consumers):
            tasks.put(None)

        tasks.join()
        result_size = result_size // 2 + (result_size % 2)
        # print('-' * 40)

    return results.get()


def main():
    my_array = [i for i in range(21)]

    result = reduce_sum(my_array)
    print('Final result: {}.'.format(result))


if __name__ == '__main__':
    main()
