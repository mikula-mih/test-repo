from dataclasses import dataclass
from typing import Iterable
import itertools

def main() -> None:
    countries = ("Germany", "France", "Italy", "Spain", "Portugal", "Greece")
    country_iter = iter(countries)

    # will raise StopIteration exception if no iterables left
    # print(next(country_iter))
    # print(next(country_iter))
    # print(next(country_iter))
    # print(next(country_iter))

    # example
    while True:
        try:
            country = next(country_iter)
        except StopIteration:
            break
        else:
            print(country)
    # use this instead
    for country in countries:
        print(country)

# `Iterable`
#   is an object that can provide you with an iterator
# `Iterator`
#   is an interval that also has a __next__
# sequences like lists, tuples, dictionaries, etc. - examples of iterables and
# they allow you to get an iterator from them

def main_abstraction():

    @dataclass(frozen=True)
    class LineItem:
        price: int
        quantity: int

        def total_price(self) -> int:
            return self.price * self.quantity

    def print_totals(items: Iterable[LineItem]) -> None:
        for item in items:
            print(item.total_price())

    line_items = [
        LineItem(1, 2),
        LineItem(3, 4),
        LineItem(5, 6),
    ]

    print_totals(line_items)


def main_custom_iterators():
    # from typing import Self

    @dataclass
    class InfiniteNumberIterator:
        num: int = 0

        # python3.11
        # def __iter__(self) -> Self:
        def __iter__(self):
            return self

        def __next__(self) -> int:
            self.num += 1
            return self.num

    @dataclass
    class NumberIterator:
        max: int
        num: int = 0

        def __iter__(self):
            return self

        def __next__(self) -> int:
            if self.num >= self.max:
                raise StopIteration
            self.num += 1
            return self.num

    for num in NumberIterator(3):
        print(num)


def main_examples() -> None:
    # Counting
    for i in itertools.count(10):
        print(i)
        if i == 15:
            break

    # Repeating
    for i in itertools.repeat(10, 4):
        print(i)

    # Accumulate
    for i in itertools.accumulate(range(1, 11)):
        print(i)

    # Get all permutations of length 2
    items = ["a", "b", "c"]
    perms = itertools.permutations(items, 2)

    # Print the permutations
    for perm in perms:
        print(perm)

    # Print all permutations as a single list
    print(list(itertools.permutations(items)))

    # Combining different iterables
    for item in itertools.chain(items, range(5)):
        print(item)

    print(list(itertools.permutations(range(3), 2)))

    # Get all combinations of length 2 (order does not matter)
    print(list(itertools.combinations(items, 2)))

    # Get all combinations with replacement of length 2
    print(list(itertools.combinations_with_replacement(items, 2)))

    # Itertools chain
    more_items = ["d", "e", "f"]
    all_items = itertools.chain(items, more_items)
    print(list(all_items))

    # Filter false
    print(list(itertools.filterfalse(lambda x: x % 2 == 0, range(10))))

    # Starmap
    print(list(itertools.starmap(lambda x, y: x * y, [(2, 6), (8, 4), (5, 3)])))

    # Tee
    a, b, c = itertools.tee(range(3), 3)
    print(list(a))
    print(list(b))
    print(list(c))


if __name__ == '__main__':
    main()
    main_abstraction()
    main_custom_iterators()
    main_examples()
