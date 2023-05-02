# Python doesn't have variables in memory, it has labels or link to containers
# in the heap
""" Python Memory Management: Stack & Heap """
# `Stack` memory for label, `Heap` for content
first_name = "Alex" # fitst_name is not a variable it's link from stack to heap
print(f'Stack memory id: {id(first_name)} | {hex(id(first_name))}')
first_name = "Petr"
print(f'   New stack id: {id(first_name)} | {hex(id(first_name))}')
print(f'     Changed id: {id(first_name.upper())} | {hex(id(first_name.upper()))}')


names = ["Alex"]
another_names = ["Alex"]

print(names == another_names) # comparing contents of memory
print(hex(id(names)))
print(hex(id(another_names)))
print(names is another_names)   # compared labels of memory

# List is mutable -> the same memory slot
print(hex(id(names)))
names.append("Jack")
print(hex(id(names)))
# Tuple is immutable
names = (["Alex", "Petr"], ["Jack"]) # tuple keeps link to a list =>
print(hex(id(names[0])))
names[0].append("John") # if list is changed
print(hex(id(names[0])))
print(names)

""" Garbage Collector """
import sys

def empty(): pass

a = empty()
b = empty()

print(sys.getrefcount(empty)) # number of referenced to an object

greetings = "Hello, Guido!"
another_greetings = greetings
print(sys.getrefcount(greetings))

del another_greetings
print(sys.getrefcount(greetings))

another_greetings = "12341235"


###

def say_hello(names: list) -> None:
    names.append("Jack")
    for name in names:
        print(f"Hi, {name}")

names = ["Alex"]
say_hello(names[:]) # send only a copy of our list
say_hello(names.copy()) # ==
say_hello(names)
print(names)

###

def say_hello(names: list = []) -> None:
    names.append("Jack")
    for name in names:
        print(f"Hi, {name}")

say_hello()
say_hello()
say_hello()

def say_hello(names: list = None) -> None:
    if names is None: names = []
    names.append("Jack")
    for name in names:
        print(f"Hi, {name}")
