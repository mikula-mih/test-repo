
from time import perf_counter

def s(n):
    return n * (n - 1) // 2

def sum_range_examples():
    n = 5
    sum(range(n))


def main():
    t0 = perf_counter()
    for _ in range(1000):
        sum_range_examples()
    t1 = perf_counter()
    for _ in range(1000):
        s(5)
    t2 = perf_counter()
    print(t1-t0)
    print(t2-t1)


if __name__ == "__main__":
    main()
