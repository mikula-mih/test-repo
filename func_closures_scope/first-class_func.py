
"""
First-Class Functions:
"A Programming language is said to have first-class functions if it treats functions as citizens."

First-Class Citizen (Programming):
"A first-class citizen (sometimes called first-class objects) in a programming language is an entity
which supports all the operations generally available to other entities. These operations typically
include being passed as an argument, returned from a function, and assigned to a variable."
"""

def square(x):
    return x * x

f = square(5)
print(square)   # <function square at 0x000000000>
print(f)        # 25

f = square  # now we can treat the var "f" as a func
print(square)   # <function square at 0x000000000>
# the same hex address
print(f)        # <function square at 0x000000000>
f(5)    # 25
"""Higer-Order Function"""
# if a func accepts other func as argument or returns func as a result, that's a
# `Higher-Order Function`

"""Map"""
def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i))
    return result

def cube(x):
    return x * x * x

cubes = my_map(cube, [1, 2, 3, 4, 5])
print(cubes)

"""Closure"""
def logger(msg):

    def log_message():
        print('Log:', msg)

    return log_message

log_hi = logger('Hi!')
log_hi()

####
def html_tag(tag):

    def wrap_text(msg):
        print('<{0}>{1}</{0}>'.format(tag, msg))

    return wrap_text

print_h1 = html_tag('h1')   # remembers the tag
# waiting to be executed
print(print_h1)     # <function html_tag.<local>.wrap_text at 0x000000000>
print_h1('Text Headline!')
print_h1('Another Headline!')

print_p = html_tag('p')
print(print_p)
print_p('Test Paragraph!')
