
""" Arguments in functions and methods """

def function(argument):
    argument += " in function"
    print(argument)

immutable = "hello"
function(immutable)
mutable = list("hello")
function(mutable)
print(immutable, '\n', mutable)
# Don't mutate function arguments. In general, try to avoid side-effects in
# functions as much as possible.

""" Variable number of arguments """

# For a variable number of positional arguments,
# the star symbol (*) is used, preceding the
# name of the variable that is packing those arguments;
def f(first, second, third):
    print(first)
    print(second)
    print(third)

l =  [1, 2, 3]
f(*l) # packing mechanism

a, b, c = [1, 2, 3]
# partial unpacking is also possible;
def show(e, rest):
    print("Element: {0} - Rest: {1}".format(e, rest))

first, *rest = [1, 2, 3, 4, 5]
show(first, rest)

*rest, last = range(6)
show(last, rest)

first, *middle, last = range(6)
first, last, *empty = (1, 2)
#
# One of the best uses for unpacking variables can be found in iteration.
USERS = [(i, f"first_name_{i}", f"last_name_{i}") for i in range(1_000)]

class User:
    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

def bad_users_from_rows(dbrows) -> list:
    """A bad case (non-pythonic) of creating ``User``s from DB rows."""
    return [User(row[0], row[1], row[2]) for row in dbrows]

def users_from_rows(dbrows) -> list:
    """Create ``User``s from DB rows."""
    return [
        User(user_id, first_name, last_name)
        for (user_id, first_name, last_name) in dbrows
    ]
#
# There is a similar notation, with two stars (**) for keyword arguments;
function(**{"key": "value"})
# is the same as
function(key="value")
# if we define a function with a parameter starting with two-star symbols, the
# opposite will happen—keyword-provided parameters will be packed into a dictionary
def function(**kwargs):
    print(kwargs)

function(key="value")
# {'key': 'value'}
