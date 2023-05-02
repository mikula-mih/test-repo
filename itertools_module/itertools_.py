import itertools
import operator

''' Itertools Module - Iterator Functions for Efficient Looping '''
# `iterator` is basically sequential data that we can iterate or loop over;
counter = itertools.count(start=5, step=-2.5)
print(next(counter), end=' ')
print(next(counter), end=' ') # goes infinitely
# built-in zip function
# ends on the shortest iterable
data = [100, 200, 300, 400]
daily_data = list(zip(itertools.count(), data))
print(daily_data)
# zip_longest function
# doesn't end until the longest iterable is exhausted;
daily_data = list(itertools.zip_longest(range(10), data))
print(daily_data)
#
counter = itertools.cycle([1, 2, 3])
counter = itertools.cycle(('On', 'Off'))
print(next(counter), end=' ')
print(next(counter), end=' ')
print(next(counter))
#
counter = itertools.repeat(2, times=3)
squares = map(pow, range(10), itertools.repeat(2))
print(list(squares))
squares = itertools.starmap(pow, [(0, 2), (1, 2), (2, 2)])
print(list(squares))
#
''' Combinations and Permutations '''
# `Combinations` are all the different ways that you can group as certain number
# of items or the order does not matter; `Permutations` order does matter;
letters = ['a', 'b', 'c', 'd']
numbers = [0, 1, 2, 3]
names = ['Mike', 'Mikula']
selectors = [True, True, False, True]

result = itertools.combinations(letters, 2)
# result = itertools.permutations(letters, 2)
# result = itertools.product(numbers, repeat=4)
# result = itertools.combinations_with_replacement(numbers, 4)
# result = itertools.islice(range(10), 5)
for item in result:
    print(item)
#
combined = itertools.chain(letters, numbers, names)
for item in combined:
    print(item)
#
result = itertools.compress(letters, selectors)
for item in result:
    print(item)
#
def lt_2(n):
    if n < 2:
        return True
    return False

result = filter(lt_2, numbers)
result = itertools.filterfalse(lt_2, numbers)
result = itertools.dropwhile(lt_2, numbers)
result = itertools.takewhile(lt_2, numbers)
for item in result:
    print(item)
#
result = itertools.accumulate(numbers)
result = itertools.accumulate(numbers, operator.mul)
for item in result:
    print(item)
#
def get_state(person):
    return person['state']
people = list()
person_group = itertools.groupby(people, get_state)
for key, group in person_group:
    print(key)
    for person in group:
        print(person)
    print()

copy1, copy2 = itertools.tee(person_group)
