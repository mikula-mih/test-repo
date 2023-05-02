""" Functions within funcitons,
    closures,
    variable scopes in Python """

# `Compiler time of Python`
# compiled & interpreted:
# a module source is first compiled to bytecode then the interpreter interpretes
# the bytecode at runtime;
# how variable scoping works depends on the separation of compile time and
# runtime behavior;
# Rule 1:
'''
    Variable Lookups happen at runtime
    Locations decided at compile time
'''


x = "global x"

def level_six():
    z = "outer z"

    def donky():
        def inner(y):
            return x, y, z

        z = "donky z"
        return inner

    def chonky():
        x = "chonky x"
        f = donky()
        return f("def y")

    return chonky()


def level_two(v):
    print(v)
    # at compile time `x` considered local var
    # nothing to return if `v` == False
    print(inner.__globals__)
    if v:
        x = "local x"
    return x


def level_three():
    # z = "outer z" # outer function scope
    print(inner.__closure__)
    def inner(y):
        return x, y, z

    z = "outer z" # outer function scope
    print(inner.__closure__)

    return inner("y arg")


def level_four():
    z = "first outer z"

    def inner(y):
        return x, y, z

    print(inner.__closure__)
    z = "second outer z" # this will be used
    print(inner.__closure__)
    # if you do not use `z` variable __closure__ will be set to None
    return inner("y arg")

# `closure` traditionally a closure is an object that wraps up a funciton with
# some kind of extra environment ( keeps a reference from being garbage collected)

def level_five(n):
    z = f"outer z {n}"

    def inner(y):
        return x, y, z

    return inner

def what_about_lambdas_and_comprehensions():
    # defining a comprehension is defining a function and immediately calling it
    l = [x * x for x in range(10)]
    # labmda is an expression
    def f(y):
        return (x, y)
    # all variable scopes for lambdas are the same as for functions
    return lambda y: (x, y)

def comprehensions_equivalent_to():
    l = [x * x for x in range(10)]
    l = list(x * x for x in range(10))
    l = list((x * x for x in range(10)))

    g = (x * x for x in range(10))

    def gen():
        for x in range(10):
            yield x * x

    g = gen()

def nonlocal_and_global():
    x = "nonlocal x"

    def f():
        nonlocal x
        # global x
        x = "overwritten nonlocal"
        return x

    print(x)
    print(f())
    print(x)


def level_seven():
    def please_dont_do_this():
        if False:
            a = None # determined to be a local variable of function

        def gen_func():
            nonlocal a
            for v in range(10):
                a = v
                yield v

        return gen_func(), lambda: a

    gen, fun = please_dont_do_this()

    # print(fun())
    # next(gen)
    # print(fun())
    # next(gen)
    # print(fun())
    # next(gen)
    # print(fun())
    # next(gen)



if __name__ == "__main__":
    # level_one()
    # level_two(False) # error
    # level_three()
    # level_four()

    # f = level_five(0)
    # g = level_five(1)
    # print(f("y arg"), g("other y arg"))

    level_six()

    # nonlocal_and_global()
    # print(x)
