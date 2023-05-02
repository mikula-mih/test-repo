
container = ['a', 'b', 'c']
string_build = ""
for data in container:
    string_build += str(data)

builder_list = []
for data in container:
    builder_list.append(str(data))
"".join(builder_list)

# Another way is to use a list comprehension
"".join([str(data) for data in container])

# or use the map function
"".join(map(str, container))


### functional approach to programming
# Map
items = [_ for _ in range(10)]
squared = list(map(lambda x: x**2, items))
print(items)
print(squared)
# mapping functions
multiply = lambda x: x*x
add = lambda x: x+x

funcs = [multiply, add]
for i in range(5):
    value = list(map(lambda x: x(i), funcs))
    print(value)

# Filter
number_list = range(-5, 5)
less_then_zero = list(filter(lambda x: x < 0, number_list))
print(less_then_zero)
# Reduce
from functools import reduce
product = reduce((lambda x, y: x * y), [1, 2, 3, 4])
print(product)
