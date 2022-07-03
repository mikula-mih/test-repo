
"""Closures"""
# A `closure` is a record storing a function together with an environment:
# a mapping associating each free variable of the function with the value or
# storage location to which the name was bound when the closure was created.
# A closure, unlike a plain function, allows the function to access those
# captured variables through the closure's regerence to them, even when the
# function is invoked outside their scope."

def outer_func_1():
    message = 'Hi'
    def inner_func():
        print(message)
    return inner_func() # return func & execute

def outer_func_2():
    message = 'Hi'
    def inner_func():
        print(message)
    return inner_func   # return func without executing

def outer_func_3(msg):
    message = msg
    def inner_func():
        print(message)
    return inner_func

outer_func_1()
print(outer_func_1)
my_func = outer_func_2()
print(outer_func_2())
print(my_func)
print(my_func.__name__)
# A `closure` is an inner function that remembers and has access to variables in
# the local scope in which it was created, even when the outer function has finished
# executing.
hi_func = outer_func_3('Hi')
hello_func = outer_func_3('Hello')
print(hi_func)
hi_func()
print(hello_func)
hello_func()

"""Closures - Logging"""
import logging
logging.basicConfig(filename='example.log', level=logging.INFO)

def logger(func):
    def log_func(*args):
        logging.info('Running "{}" with arguments {}'.format(func.__name__, args))
        print(func(*args))
    return log_func

def add(x, y):
    return x+y

def sub(x, y):
    return x-y

add_logger = logger(add)
sub_logger = logger(sub)

add_logger(3, 3)
add_logger(4, 5)

sub_logger(10, 5)
sub_logger(20, 10)
