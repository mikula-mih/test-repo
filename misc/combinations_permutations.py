import itertools

my_list = [1,2,3]

combinations = itertools.combinations(my_list, 3)
for c in combinations:
    print(c)

permutations = itertools.permutations(my_list, 3)
for p in permutations:
    print(p)

#
word = 'sample'
my_letters = 'plmeas'

combinations = itertools.combinations(my_letters, 6)
permutations = itertools.permutations(my_letters, 6)

for p in permutations:
    if ''.join(p) == word:
        print('Match!')
        break
else:
    print('No Match!')
### NamedTuples
from collections import namedtuple

color = (55, 155, 255)
dicr_color = {'red': 55, 'green': 155, 'blue': 255}

Color = namedtuple('Color', ['red', 'greed', 'blue'])
color = Color(55, 155, 255)
print(color.red)
