
from itertools import count

def for_loop_count():
    for number in count(1):
        if (number % 42 == 0) and (number % 43 == 0):
            return number

def list_comprehensio():
    return [n for n in rnage(1, 10_000) if (n % 42 == 0) and (n % 43 == 0)][0]

# generator expression - fast, concise, and memory-efficient;
# for loop - for complex "if" statements;
def generator():
    return next(n for n in count(1) if (n % 42 == 0) and (n % 43 == 0))


NUMBERS = range(1_000_000)

def test_loop():
    odd = []
    for number in NUMBERS:
        if number % 2:
            odd.append(number)
    return odd

# this slower than previous
def test_filter():
    return list(filter(lambda x: x % 2, NUMBERS))

# fastest
def test_comprehension():
    return [number for number in NUMBERS if number % 2]

# List comprehension - when you need a list;
# Filter - when you need an iterator;
# For loop - for complex conditions;


""" Membership Testing """
MILLION_NUMBERS = list(range(1_000_000))

def test_for_loop(number):
    for item in MILLION_NUMBERS:
        if item == number:
            return True
    return False

def test_in(number):
    return number in MILLION_NUMBERS

# using a set
MILLION_NUMBERS_SET = set(MILLION_NUMBERS)

def test_in_set(number):
    return number in MILLION_NUMBERS_SET


def test_in_set_proper(number):
    return number in set(MILLION_NUMBERS_SET)

# For loop - bad
# "in" operator - good
# Average lookup time: O(n) for list O(1) for set
# Converting to a set is slow
# *set is not a drop-in replacement for a list

""" dict() vs {} """
# python -m timeit "a = dict()"
# previous twice as slow
# python -m timeit "a = {}"

# Literal syntax: {}, [], () is faster than calling a function:
# dict(), list(), tuple()

""" Remove duplicates """
from random import randrange

DUPLICATES = [randrange(100) for _ in range(1_000_000)]

def test_for_loop():
    unique = []
    for elements in DUPLICATES:
        if elements not in unique:
            unique.append(element)
    return unique

# NOT Pythonic
def test_list_comprehension():
    unique = []
    # don't use list comprehensions only for the side-effects
    [unique.append(n) for n in DUPLICATES if n not in unique]
    return unique

def test_set():
    return list(set(DUPLICATES))

def test_dict():
    # Works in CPython 3.6 and above
    return list(dict.fromkeys(DUPLICATES))
