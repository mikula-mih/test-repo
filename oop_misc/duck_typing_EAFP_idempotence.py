
""" Duck Typing """

class Duck:

    def quack(self):
        print('Quack, quack')

    def fly(self):
        print('Flap, Flap!')


class Person:

    def quack(self):
        print("I'm Quacking Like a Duck!")

    def fly(self):
        print("I'm Flapping my Arms!")


def quack_and_fly(thing):
    #'''
    # Not Duck-Typed(Non-Pythonic)
    if isinstace(thing, Duck):
        thing.quack()
        thing.fly()
    else:
        print('This has to be a Duck!')
    #'''

    #'''
    # LBYL (Non-Pythonic)
    if hasattr(thing, 'quack'):
        if callable(thing.quack):
            thing.quack()

    if hasattr(thing, 'fly'):
        if callable(thing.fly):
            thing.fly()
    #'''

    #'''
    """ Easier to Ask Forgiveness then Permission (EAFP) """
    # Pythonic
    try:
        thing.quack()
        thing.fly()
        thing.bark()
    except AttributeError as e:
        print(e)
    #'''

    print()

d = Duck()
quack_and_fly(d)

p = Person()
quack_and_fly(p)


""" Idempotence """
# the property of certain operations in mathematics and computer science, that
# can be applied multiple times without changing the result beyond the initial
# application;
# f(f(x)) = f(x)

def add_ten(num):
    return num + 10

print(add_ten(10))
print(abs(abs(-10))) # Idempotent

# Idempotence in HTTP methods
# GET - idempotent
# PUT - idempotent
# POST - not idempotent
# DELETE - idempotent
