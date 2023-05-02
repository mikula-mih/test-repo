"""
LEGB
Local, Enclosing, Global, Built-in
"""

x = 'global x'

def test():
    y = 'local y'
    print(y) # local scope
    x = 'local x'
    print(x) # global scope

test()
print(x) # global scope

def change():
    global x
    x = 'changed global x'
    print(x)

change()
print(x)

####

m = min([5, 1, 4, 2, 3]) # built-in func in Python
print(m)

import builtins
print(dir(builtins))

###
# Global
# !!! play with uncommenting of x var !!!

x = 'global x'

def outer():
    x = 'outer x'

    def inner(): # enclosing scope
        nonlocal x # change the state of closures
        x = 'inner x'
        print(x)

    inner()
    print(x)

outer()
print(x)
