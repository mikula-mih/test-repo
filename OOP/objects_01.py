print(type("Hello World"), type(42))

"""
>>> 1.Everything in Python is an object.
>>> 2.Every object is defined by being an instance of at least one class.

>>> A variable is a reference to an object.

`The terms 'class' and 'type' are an example of two names referring to
the same concept.`

>>> type()  # the type of the object the variable currently references
>>> id()    # id of a variable shows the ID of the object the variable refers to.

# the variable doesn't have a type of its own; it's nothing more than a name.
# Python doesn't prevent us from attempting to use non-existent methods of objects.
"""
#
""" Type checking """
# specified that argument values for the n parameter should be integers
def odd(n: int) -> bool:     # the annotations `type hints`
# add -> syntax to a function (or a class method) definition
# to explain the expected return type.
    return n % 2 != 0

def main() -> None:
    try:
        print(odd("Hello World"))
    except TypeError:
        print(odd(n) for n in range(10))

if __name__ == "__main__":
    main()

print(odd(n) for n in range(10))
print(*(odd(n) for n in range(10))) # unpacking the generator
# pip install mypy
# >>> mypy --strict <file>.py
# mypy tool is commonly used to check the hints for consistency
""" Creating Python classes """
class MyFirstClass:
    pass
# >>> python -i <file>.py
# the -i argument tells Python to `run the code and then drop to the interactive interpreter`
a = MyFirstClass()  # instantiate two object from the new class,
b = MyFirstClass()  # assigning the object variable names a and b
# calling a class will create a new object
print(a, b, a is b)
""" Adding attributes """
# create an empty Point class with no data or behaviours.
class Point: pass
# create two instances of that class
p1 = Point()
p2 = Point()
# assign a value to an attribute on an object
p1.value = "data type: str"
"""syntax:
<object>.<attribute> = <value>
`dot notation`
"""
# the value can be anything: a Python primitive,
# a built-in data type, or another object, function or another class!
p1.x, p1.y, p2.x, p2.y = (x for x in range(4))
print(p1.x, p1.y)
print(p2.x, p2.y)
