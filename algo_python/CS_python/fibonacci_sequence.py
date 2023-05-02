

def fib1(n: int) -> int:
    # RecursionError: maximum recursion depth exceeded
    return fib1(n - 2) + fib1(n - 1) # infinite recursion

def fib2(n: int) -> int:
    if n < 2: # base case
        return n
    return fib2(n - 2) + fib2(n - 1) # recursive case

# `Memoization` is a technique in which you store the results of computational
#   tasks when they are completed so that when you need them again, you can
#   look them up; Donald Michie, a famous British computer scientist;
from typing import Dict

memo: Dict[int, int] = {0: 0, 1: 1} # our base cases

def fib3(n: int) -> int:
    if n not in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2) # memoization
    return memo[n]

# `Automatic memoization`
# built-in decorator for memoizing any function automagically
from functools import lru_cache

@lru_cache(maxsize=None)
def fib4(n: int) -> int: # same definition as fib2()
    if n < 2: # base case
        return n
    return fib4(n - 1) + fib4(n - 2) # recursive case

# old-fashioned == the most efficient version
def fib5(n: int) -> int:
    if n == 0: return n # special case
    last: int = 0 # initially set to fib(0)
    next: int = 1 # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
    return next

# Generators
from typing import Generator

def fib6(n: int) -> Generator[int, None, None]:
    yield 0 # special case
    if n > 0: yield 1 # special case
    last: int = 0 # initially set to fib(0)
    next: int = 1 # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
        yield next # main generation step

if __name__ == "__main__":
    # print(fib1(5))

    print(f"{fib2(5)=}")
    print(f"{fib2(10)=}")
    print('')
    print(f"{fib3(5)=}")
    print(f"{fib3(50)=}")
    print('')
    print(f"{fib4(5)=}")
    print(f"{fib4(50)=}")
    print('')
    print(f"{fib5(5)=}")
    print(f"{fib5(50)=}")
    print('')
    for i in fib6(50):
        print(i)
