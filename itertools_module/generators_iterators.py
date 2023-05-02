
"""
Generators vs Iterators
"""
# `Iterators` an object that enables a programmer to traverse a container,
# particularly lists.
# `Generators` a routine that can be used to control the iteration behaviour
# of a loop. A generator is very similar to a function that returns an array.
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
import sys
print(sys.getsizeof(x)) # 152
# return an iterator --> smaller size
print(sys.getsizeof(range(1, 11))) # 48
# iterator allows to access items without storing them in some data structure

y = map(lambda i: i**2, x)
# map() does not store the list;
print(y) # <map object at 0x0000000000000000000>
print(list(y))
#
print(sys.getsizeof(list(y))) # 56 | list stored
print(sys.getsizeof(y)) # 48 | iterator
# looping through map() with next() function
#
# !!! have to map() again because we've looped through already
y = map(lambda i: i**2, x)
print(next(y)) # iterator has a next() method
print(y.__next__()) # dunder method
print(next(y))
print("For Loop Starts")
for i in y:
    print(i)
#
while True:
    try:
        value = next(y)
        print(value)
    except StopIteration:
        print('Done')
        break
# for `range` you have to use iter() !!!!
x = range(1, 11)
print(x) # range(1, 11)
print(next(iter(x)))
print(x.__iter__()) # <range_iterator object at 0x0000000000000000000>
print(next(x.__iter__())) # returns first num in range
# !!! no next() funtion for `range`
for i in iter(x):
    print(i, end=' ')
print() # for next line
#
""" Creating `Legacy Iterators` """

class Iter:

    def __init__(self, n):
        self.n = n

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        self.current += 1
        if self.current >= self.n:
            raise StopIteration
        return self.current

x = Iter(5)
for i in x:
    print(i, end=' ')
print() # for next line
#
""" Creating Generators """
# use `yield` keyword instead of `return`
def gen(n):
    for i in range(n):
        yield i
# when the yield keyword is hit, it pauses the execution of the function and
# returns the value to whatever is iterating through this generator object;
for i in gen(5):
    print(i, end=' ')
print() # for next line
# doing the same manually without for loop
x = gen(5)
print(next(x))
print(next(x))
def yielding():
    yield 1 # pauses the execution of func returns 1
    yield 2
    yield 3
x = yielding()
print(next(x), 'yielded')
print(next(x), 'yielded')
# WHAT ARE THE USE CASES !!!
# the usecase of a generator: you can loop through a sequence or some large amount
# of data without needing to store all of it;
def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row # yields only one row of the file at a time

""" Generator Comprehensions """
x = (i for i in range(10))
print(x) # <generator object <genexpr> at 0x0000000000000000000>
print(next(x))
print(next(x))
print(next(x))
