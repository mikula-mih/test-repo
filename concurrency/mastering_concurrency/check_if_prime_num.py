from timeit import default_timer as timer
from math import sqrt
import multiprocessing
import concurrent.futures

class IsPrime:
    def __init__(self, input: list):
        self.input = input

    @staticmethod
    def is_prime(x) -> bool:
        if x < 2:
            return False

        if x == 2:
            return True

        if x % 2 == 0:
            return False

        limit = int(sqrt(x)) + 1
        for i in range(3, limit, 2):
            if x % i == 0:
                return False

        return True

    @staticmethod
    def show_result(exec_type: str, result: list, start: float) -> None:
        print(f'Result {exec_type}: {result}')
        print(f"Took: {(timer() - start):.3f} seconds.")

    def sequential_execution(self) -> None:
        start = timer()
        result = list()
        for i in self.input:
            if self.is_prime(i):
                result.append(i)

        self.show_result("seq", result, start)

    def concurrent_execution(self, n_workers=20) -> None:
        start = timer()
        result = []

        with concurrent.futures.ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = [executor.submit(self.is_prime, i) for i in self.input]
            completed_futures = concurrent.futures.as_completed(futures)

            sub_start = timer()

            for i, future in enumerate(completed_futures):
                if future.result():
                    result.append(future.result())

        sub_duration = timer() - sub_start
        print('Sub took: %.4f seconds.' % sub_duration)
        self.show_result("conc", result, start)



if __name__ == '__main__':
    input = [i for i in range(10 ** 13, 10 ** 13 + 500)]
    prime = IsPrime(input)
    prime.sequential_execution()

    for n_workers in range(1, multiprocessing.cpu_count() + 1):
        prime.concurrent_execution(n_workers)
        print('_' * 20)
