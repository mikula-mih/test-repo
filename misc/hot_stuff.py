
''' Python's sharpest corner: += '''

def tuple_what():
    # a_tuple = (1, 2)
    # a_tuple[0] += 1 # obvious error, tuple immutable
    # but not tuple's elements
    pros_and_cons = (["smth"], ["real interesting"])

    pros = pros_and_cons[0]
    pros += ["cool"] # fine

    try:
        pros_and_cons[0] += ["will still append???"] # maybe?
    except TypeError:
        print("Error!")
    print(pros_and_cons) # hm?


def plusequals_meaning(x, y):
    # x += y
    result = x.__iadd__(y)
    x = result

    # x[0] += y
    result = x[0].__iadd__(y) # calls __getitem__
    x[0] = result # calls __setitem__

    # x.val += y
    result = x.val.__iadd__(y) # calls __getattr__
    x.val = result # calls __setattr__


class BadList(list):
    def __add__(self, other):
        print("running custom add")
        return BadList(super(BadList, self).__add__(other))

    def __iadd__(self, other):
        print("running custom iadd")
        return self + other


def plusequals_may_change_pointers():
    x = 1
    print(id(x))
    x += 1
    print(id(x), "changed")

    x = []
    print(id(x))
    x += [1]
    print(id(x), "not changed")

    bad = BadList()
    print(bad, "before append")
    bad += [1, 2, 3] # manual extend
    append_some_to_list(bad) # might do nothing?
    print(bad, "after append")


def append_some_to_list(l):
    l += [4, 5, 6]



''' the Best way to check for optional arguments in python '''

def normal(arr: list, x: int = None, options: dict = None):
    x = x if x is not None else len(arr)

    if options is None:
        options = {"option": "value"}

# `sentinel` is an object whose sole purpose is to check whether or not something
# is the sentinel value;
MISSING = object()

def tricky(x=MISSING):
    if x is MISSING:
        x = 42
    elif x is None:
        x = 43


def main_tuple():
    tuple_what()


if __name__ == '__main__':
    main_tuple()
