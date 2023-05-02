

# PEP-255
# `generator` is to create an object that is iterable,
# and, while it's being iterated, will produce the elements it contains,
# one at a time. The main use of generators is to save memory;
# enables lazy computations or heavyweight objects in memory

class PurchasesStates:

    def __init__(self, purchases):
        self.purchases = iter(purchases)
        self.min_price: float = None
        self.max_price: float = None
        self._total_purchases_price: float = 0.0
        self._total_purchases = 0
        self._initialize()

    def _initialize(self):
        try:
            first_value = next(self.purchases)
        except StopIteration:
            raise ValueError("no value provided")

        self.min_price = self.max_price = first_value
        self._update_avg(first_value)

    def process(self):
        for purchases_value in self.purchases:
            self._update_min(purchases_value)
            self._update_max(purchases_value)
            self._update_avg(purchases_value)
        return self

    def _update_min(self, new_value: float):
        if new_value < self.min_price:
            self.min_price = new_value

    def _update_max(self, new_value: float):
        if new_value > self.max_price:
            self.max_price = new_value

    @property
    def avg_price(self):
        return self._total_purchases_price / self._total_purchases

    def _update_avg(self, new_value: float):
        self._total_purchases_price += new_value
        self._total_purchases += 1

    def __str__(self):
        return (
            f"{self.__class__.__name__}({self.min_price}, "
            f"{self.max_price}, {self.avg_price})"
        )

    '''
    If you run it with a rather large dataset, it will take a while
    to complete, and it might even fail if the dataset is large enough
    as to not fit into the main memory
    '''
    # def _load_purchases(filename):
    #     purchases = []
    #     with open(filename) as f:
    #         for line in f:
    #             *_, price_raw = line.partition(",")
    #             purchases.append(float(price_raw))
    #
    #     return purchases


    def _load_purchases(filename):
        with open(filename) as f:
            for line in f:
                *_, price_raw = line.partition(",")
                yield float(price_raw)

# Working with iterables allows us to create powerful abstractions that are
# polymorphic with respect to for loops;
# As long as we keep the iterable interface,
# we can iterate over that object transparently;

""" Generator expressions """
# >>> [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
# >>> (x**2 for x in range(10))
# <generator object <genexpr> at 0x...>
# >>> sum(x**2 for x in range(10))
# 285

""" Iterating idiomatically:
    Idioms for iteration
"""
# >>> list(enumerate("abcdef"))
# [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f')]

class NumberSequence:

    def __init__(self, start=0):
        self.current = start

    def __next__(self):
        current = self.current
        self.current += 1
        return current

    def __iter__(self):
        return self

# >>> list(zip(SequenceOfNumbers(), "abcdef"))
# [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f')]
# >>> seq = SequenceOfNumbers(100)
# >>> next(seq)
# 100
# >>> next(seq)
# 101
""" next() function """
# >>> word = iter("hello")
# >>> next(word)
# 'h'
# >>> ...
# >>> next(word)
# 'o'
# >>> next(word)
# Traceback (most recent call last):
# File "<stdin>", line 1, in <module>
# StopIteration
# >>>
#
# >>> next(word, "default value")
# 'default value'

""" using a generator """
def sequence(start=0):
    while True:
        yield start
        start += 1

seq = sequence(10)
next(seq) # 10
print(list(zip(sequence(), "abcdef")))
# [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f')]
