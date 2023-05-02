
""" Positional-only and keyword-only arguments in Python """

def f(a, b, c):
    print(f'{a=}, {b=}, {c=}')

def calling_normal_args_example():
    f(1, 2, 3)
    f(a=1, b=2, c=3)
    f(c=3, a=1, b=2)
    f(1, c=3, b=2)

def g(a, b, *, kw_only):
    print(f'{a=}, {b=}, {kw_only}')

"""
EVERYTHING after a `*` or `*args` must be a `keyword arg`
`*args` eats all remaining positional arguments
"""

def force_keyword_argument():
    g(1, b=2, kw_only=3)
    # passing arg after * as a positional will return error
    # g(1, 2, 3) # SyntaxError

def g0(a, b, *args, kw_only):
    print(f'{a=}, {b=}, {args=}, {kw_only}')

def force_keyword_argument_0():
    g0(1, 2, 3, 4, kw_only=3)
    g0(1, 2, kw_only=3)

# Keyword only arguments are most often used as options or settings that
# slightly vary or modify the behavior of some code;

def combine(a, b, validator=None):
    result = []
    result.extend(a)
    result.extend(b)
    if validator is not None:
        if not all(map(validator, result)):
            raise ValueError("invalid elements")
    return result

def use_combine():
    combine("sub", "scribe")

# USE CASE:
def place_order(*, item, price, quantity):
    print(f" {quantity} units of {item} at {price} price")

def what_could_go_wrong():
    place_order(item="SPX", price=4500, quantity=10000)




# TEMPLATE MAIN:
def f(pos_only, /, pos_or_kw, *, kw_only, **kwargs):
    # **kwargs to catch all remaining kwargs
    pass

############

# USE CASE:
def check_truthy(x, /):
    if not x:
        raise ValueError(f"expected truthy object, got: {x}")

def power_mod(x, y, /, *, mod):
    return (x ** y) % mod # note: very slow

def force_positional_arguments():
    z = power_mod(3, 50, mod=17)

def dataclass(cls=None, /, *, init=True, repr=True, many_more=...):
    pass

# Speed test | position args are faster
from timeit import timeit
def speed_differences():
    def func(a, b, c):
        pass

    trials = 10 ** 7
    display_scale = 10 ** 9 # nanoseconds

    t1 = timeit(stmt="func(1, 2, 3)", globals={'func': func}, number=trials)
    t2 = timeit(stmt="func(a=1, b=2, c=3)", globals={'func': func}, number=trials)
    t3 = timeit(stmt="func(c=3, a=1, b=2)", globals={'func': func}, number=trials)
    t4 = timeit(stmt="func(1, c=3, b=2)", globals={'func': func}, number=trials)

    def func(a, b, c, /):
        pass

    t5 = timeit(stmt="func(1, 2, 3)", globals={'func': func}, number=trials)

    def func(*, a, b, c):
        pass

    t6 = timeit(stmt="func(a=1, b=2, c=3)", globals={'func': func}, number=trials)
    t7 = timeit(stmt="func(c=3, b=2, a=1)", globals={'func': func}, number=trials)

    print("normal func")
    print(f'{t1=:.2f}\t\t func(1, 2, 3)')
    print(f'{t2=:.2f}\t\t func(a=1, b=2, c=3)')
    print(f'{t3=:.2f}\t\t func(c=3, a=1, b=2)')
    print(f'{t4=:.2f}\t\t func(1, c=3, b=2)')
    print()

    print("pos only")
    print(f'{t5=:.2f}\t\t func(1, 2, 3)')
    print()

    print("kw only")
    print(f'{t6=:.2f}\t\t func(a=1, b=2, c=3)')
    print(f'{t7=:.2f}\t\t func(c=3, b=2, a=1)')



if __name__ == "__main__":
    force_keyword_argument()
    force_keyword_argument_0()
    speed_differences()
