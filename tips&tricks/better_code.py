
""" Ternary operators / conditionals """
condition = True

if condition:
    x = 1
else:
    x = 0
# the same as
x = 1 if condition else 0

print(x)

""" BIG NUMS """
num = 1_000_000_000
print(f'{num:,}') # 1,000,000,000
""" Contex Manager """
f = open('some_file.txt', 'r')
file_contents = f.read()
f.close()
#
with open('some_file.txt', 'r') as f:
    file_contents = f.read()

words = file_contents.split(' ')
word_count = len(words)
print(word_count)

""" enumerate func && unpacking """
# if you want to keep an eye on the loop you are currently on
names = ['a', 'b', 'c']
heroes = ['A', 'B', 'C']
# returns both an index and an item of a list we are looping over
for index, name in enumerate(names, start=1): # default start=0
    print(index, name)

for name, hero in zip(names, heroes): # can zip more than 2 lists
    print(f'{name} is actually {hero}')

for value in zip(names, heros):
    print(value) # returns tuples

# !!! `zip` will stop at the shortest lists index, when it is exhausted
# but you can use zip longest function from iter tools module

""" unpacking """
a, _ = (1, 2) # _ shows that we are not planning to use that variable further in our code
print(a)

a, b, *c = (1, 2, 3, 4, 5) # `*` unpacks the rest into `c` variable, meaning a List
a, b, *_ = (1, 2, 3, 4, 5) # `*_` throws away the rest
a, b, *_, d = (1, 2, 3, 4, 5) # `*_` throws away untill the last

""" Getting & Setting an Attributes on Object """
class Person():
    pass

person = Person()

# Dynamically add some attributes
person.first = "first"
person.last = "last"
#
setattr(person, 'first_attr', 'content_attr')
print(person.first_attr)
first_key = 'first'
first_val = 'first_value'
setattr(person, first_key, first_val)
print(person.first)

first = getattr(person, first_key)
#
person = Person()
person_info = {'first': '1_val', 'last': 'last_val'}

for key, value in person_info.items():
    setattr(person, key, value)

for key in person_info.keys():
    print(getattr(person, key))

""" Input secret information """
from getpass import getpass
username = input('Username: ')
password = getpass('Password: ') # hides keys

print('Logging In...')

""" flags """
# `python -m`
# search for module
# python -m <module> -c <command> -n <network>
# python -m smtpd -c DebuggingServer -n localhost:1025

""" .Env """
# export DB_USER=""
import os
db_user = os.environ.get('DB_USER')

""" 0.1 + 0.2 != 0.3 """
# floats IEEE_754
def addition_fail():
    print(".1 + .2:", .1 + .2) # 0.30000000000000004
    print(".1 + .2 == .3", .1 + .2 == .3) # False

    print(f".1:\t\t{pretty_float_bits(.1)}")
    print(f".2:\t\t{pretty_float_bits(.2)}")
    print(f".3:\t\t{pretty_float_bits(.3)}")
    print(f".1+.2:\t{pretty_float_bits(.1 + .2)}")

def float_to_bin(f) -> str:
    # d for double precision (64 bit) floating point,
    # > for big-endian (the way we usually write numbers in math)
    fmt = ">d"
    bz = struct.pack(fmt, f)
    return "".join(f"{b:08b}" for b in bz)

def every_n_characters(s, n):
    for i in range(0, len(s), n):
        yield s[i:i + n]

# 64 bit float
# 1{sign}11{exponent}52{fraction}

def one_and_negative_one():
    print(f"1.:\t\t{pretty_float_bits(1.)}")
    print(f"-1.:\t{pretty_float_bits(-1.)}")

def zero_and_negative_zero():
    print(f"0.:\t\t{pretty_float_bits(0.)}")
    print(f"-0.:\t{pretty_float_bits(-0.)}")
    x, y = 0., -0.
    print("0. == -0.?", x == y) # True
    print("0. is -0.?", x is y) # False

    x, y = 0, -0
    print("0 is 0?", x is y) # True

def infinities():
    print(f'2**1023:\t{pretty_float_bits(2. ** 1023)}')
    print(f'2**1024:\t{pretty_float_bits(2. ** 1023 * 2)}')
    print(f'inf:\t\t{pretty_float_bits(float("inf"))}')
    print(f'-inf:\t\t{pretty_float_bits(float("-inf"))}')

def nans():
    print(f'nan:\t\t{pretty_float_bits(float("nan"))}')
    print(f'inf*0:\t\t{pretty_float_bits(float("inf") * 0.)}')
    my_nan = bits_to_float("0111111111111000000000000001000000000000010000000000000000000000")
    print(f'mynan:\t\t{pretty_float_bits(my_nan)}')

    print("nan == nan?", float("nan") == flaot("nan"))

def denormalized_numbers():
    print(f'2**-1022:\t{pretty_flaot_bits(2 ** -1022)}')
    print(f'2**-1023:\t{pretty_flaot_bits(2 ** -1023)}')
    print(f'2**-1024:\t{pretty_flaot_bits(2 ** -1024)}')
    print(f'2**-1074:\t{pretty_flaot_bits(2 ** -1074)}')
    print(f'2**-1075:\t{pretty_flaot_bits(2 ** -1075)}')
    print(f'2**-1076:\t{pretty_flaot_bits(2 ** -1076)}')

def almost_equal(x, y, eps=10 ** -6):
    return abs(x - y) < eps

def exact_repr():
    print(repr(Decimal(".1")))
    print(Decimal(".1") + Decimal(".2") == Decimal(".3"))

""" Memoization """
# `Memoization` is an optimization technique used primarily to speed up computer
# programs by storing the results of expensive function calls and returning the
# cached result when the same inputs occur again;
ef_cache = {}
def expensive_func(num):
    if num in ef_cache:
        return ef_cache[num]
    result = num * num
    ef_cache[num] = result
    return result

""" List Slicing """
# `Slicing` is a way of extracting certain elements from the list
my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#          0, 1, 2, 3, 4, 5, 6, 7, 8, 9
#        -10,-9,-8,-7,-6,-5,-4,-3,-2,-1
# list[start:end:step]
print my_list[-10:-1] # end_index not inclusive
print my_list[1:-2:2]
print my_list[2:-1:-1] # negative step == in reverse;
# returns [] because of the negative step between index 2 and -1
print my_list[-1:2:-1] # returns [9, 8, 7, 6, 5, 4, 3]
print my_list[::-1] # complete list in reverse
print my_list[::] # all

#############################
""" IDE """
# set auto conversion of tabs to spaces
# set `pylint` that catches mistakes

""" Modules """
# don't use names from standard library for your modules
from math import radians, sin
radians = radians(90) # !!! mistake assignment to 'radians' var
print(sin(radians))
rad45 = radians(45) # we give an error, after previous assignment 'radians'
print(rad45)

""" Default arguments """
def add_employee(emp, emp_list=[]): # not creating a new list each time we create a func
    emp_list.append(emp)
    print(emp_list)

def add_employee_NEW(emp, emp_list=None):
    if emp_list is None:
        emp_list = []
    emp_list.append(emp)
    print(emp_list)

# Default arguments are executed once, when the function is created and not each
# time the function is called.
def display_time(time=datetime.now()):  # will give timestamp of first call for every next run
    print(time.strftime('%B %d, %Y %H:%M:%S'))

""" Iterators """
names = ['a', 'b', 'c']
heroes = ['A', 'B', 'C']

identities = zip(names, heroes)

print(identities) # in python2 returns list of tuples
# in python3 return <zip object at 0x000000000>
print(list(identities)) # use this instead

for identity in identities:
    print('{} is actually {}!'.format(identity[0], identity[1]))

""" Imports """
# dont use * on imports
from os import * # bad practice
# this will make your code hard to debug in big files
# introduces error into our code
from html import *
from glob import * # html.escape will be overwritten by glob.escape
# both of the modules have an `escape` function
print(help(escape)) # wiil show functions helper for module glob
from glob import escape as g_escape # better practice

########
