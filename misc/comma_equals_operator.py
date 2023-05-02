
def do_something():
    x = 1
    y = 2

    x, y = y, x
    (x, y) = [y, x] # pattern matching
    x, = y # comma for iterable tuple

def smthing():
    primes = {2, 3, 5, 7, 11}
    evens = {2, 4, 6, 8, 10}

    intersection = primes.intersection(evens)
    x = intersection.pop()
    print(x)


# What is the difference between "==" and "is"?
# "==" checks for equality
# "is" checks for identity

if __name__ == '__main__':
    smthing()
