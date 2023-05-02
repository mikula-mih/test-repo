
def multiple_assignments():
    a = b = c = d = []
    # tmp = [] # temporary variable -> a = tmp, b = tmp |=> the same
    print(a, b, c, d)
    print(a is b)
    a, b = [], []
    print(a is b)

def tuple_assignment():
    a, b = 1, 2
    print(a, b)

def tricky_assignments():
    a, b = a[:] = [[]], []
    # tmp = [[]], []
    # a, b = tmp |=> a = [[]]
    # a[:] = tmp |=> a is a member of itself `...`
    print(a, b)
    print(a is a[0]) # cyclic reference

def tricky_assignments2():
    a, b = a[b] = a = [1, 2, 3], 2
    # assignment from left to right
    print(a, b)

# Python3.9
def multiple_assignment_expressions():
    (a := (b := (c := (d := 0)))) # := reterns value back to you
    # from right to left
    print(a, b, c, d)

def main():
    pass
