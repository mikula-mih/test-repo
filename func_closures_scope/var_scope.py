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
