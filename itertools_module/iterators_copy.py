
def list_example():
    l = [1, 2, 3, 4]

    for x in reversed(l): # copy?
    # for x in l[::-1]:
    # for idx in range(len(l) -1, -1, -1):
        # print(l[idx])
        print(x)

# REVERSED does not make a copy of your sequence
print(reversed([1, 2, 3, 4]))
# receive <list_reverseiterator object at 0x00000>


class reversed:
    def __init__(self, seq):
        self.seq = seq
        self.n = len(seq) - 1
        if not hasattr(seq, '__getitem__'):
            raise TypeError("not reversible")

    def __iter__(self):
        return self

    def __next__(self): # called by next()
        if self.n == -1:
            raise StopIteration
        n = self.n
        self.n = n - 1
        return self.seq[n]


# generator
def reversed(seq):
    n = len(seq) - 1
    if not hasattr(seq, '__getitem__'):
        raise TypeError("not reversible")
    while n != -1:
        yield seq[n]
        n -= 1


def copy_or_no_copy():
    l = [("a", 1), ("b", 2), ("c", 3)]
    d = dict(l)

    makes_a_copy = [
        dict(l),
        frozenset(l),
        list(l),
        set(l),
        sorted(l),
        tuple(l),
        l[::-1], # or any slice
        [x for x in l],
    ]

    for x in makes_a_copy:
        print(x)

    doesnt_make_a_copy = [
        enumerate(l),
        filter(None, l),
        iter(l),
        map(lambda x: x, l),
        reversed(l),
        zip(l, l),
        d.keys(),
        d.values(),
        d.items(),
        (x for x in l),
    ]

    for x in doesnt_makes_a_copy:
        print(x)


def numpy_example():
    import numpy as np

    arr = np.array([1, 2, 3])
    rev = arr[::-1] # slicing a list amlost always makes a copy
    # numpy doesn't make a copy
    # achieves this using strides
    print(arr.data)
    print(rev.data)


def copy_example():
    d = {"a": 1, "b": 2, "c": 3}

    # won't work
    # for char, val in d.items():
    #     d[char.upper()] = val
    # the solution is to make a copy
    for char, val in list(d.items()):
        d[char.upper()] = val

    print(d)
