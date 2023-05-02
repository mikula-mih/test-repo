
""" In Python, method is formatted identically to a function:
    the `def` keyword & the name of the method
    set of parentheses containing the parameter list & terminated with a colon
    next line is indented to contain the statements inside the method.
These statements can be arbitrary Python code operating on the object
    itself and any parameters passed in, as the method sees fit.
"""
# add behavior to our class
class Point:
    # model a couple of actions on our Point class
    # `method` called reset
    def reset(self):
        self.x = 0
        self.y = 0

p = Point()
p.reset()
print(p.x, p.y)
"""The `self` argument to a method is a reference to the object that the method
    is being invoked on. The object is an instance of a class,
    and this is sometimes called the `instance variable`.
We can access attributes and methods of that object via this variable.
The `self` parameter refers to a specific instance of the class.
When you call the method on two different objects, you are calling the same
    method twice, but passing two different objects as the `self` parameter.
"""
# Instead of calling the method on the object, we could invoke the function as
# defined in the class, explicitly passing our object as the `self` argument.
p = Point()
Point.reset(p)  # not really a good programming practice
import math
# include a method that accepts another Point object as input
class Point:
    # define a class with two attributes, x, and y, and three separate methods
    def move(self, x: float, y: float) -> None: # accepts two arguments
        self.x = x  # set a value on the self object
        self.y = y

    def reset(self) -> None:    # reset() method calls the move() method
        self.move(0, 0)

    def calculate_distance(self, other: "Point") -> float:
        # method computes the Euclidean distance between two points
        return math.hypot(self.x - other.x, self.y - other.y)

p1 = Point()
p2 = Point()
p1.reset()
p2.move(5, 0)
# the program will bail if the expression after `assert`
# evaluates to False (or zero, empty, or None)
assert p1.calculate_distance(p2) == p2.calculate_distance(p1)
print(f"{p1.calculate_distance(p2)=}")
""" Initializing the object """
# the concept of a `constructor`,
# a special method that creates and initializes the object when it is created
# Python has a `constructor` and `initializer`
# >>> `constructor` method __new__()
# >>> `initializer` method __init__()
# The `leading and trailing double underscores` mean this is a
# special method that the Python interpreter will treat as a special case
class Point():
    # include type annotations on the method parameters and result values
    def __init__(self, x: float, y: float) -> None:
        self.move(x, y)
    # after each parameter name, include the expected type of each value
    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    # at the end of the definition, include -> operator and the type returned by the method
    def reset(self) -> None:
        self.move(0, 0)

    def calculate_distance(self, other: "Point") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
# constructing a Point instance
point = Point(3, 5) # initialization parameters
print(point.x, point.y)
""" Explaining yourself with docstrings
    docstrings are quite long and span multiple lines (the style guide suggests
    that the line length should not exceed 80 characters), which can be
    formatted as multi-line strings, enclosed in
    matching triple apostrophe (''')
    or
    triple quote (\""") characters
"""
# tools like `doctest` can locate and confirm these examples are correct
class Point:
    """
    Represents a point in two-dimensional geometric coordinates

    >>> p_0 = Point()
    >>> p_1 = Point(3, 4)
    >>> p_0.calculate_distance(p_1)
    5.0
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Initialize the position of a new point. The x and y
        coordinates can be specified. If they are not, the
        point defaults to the origin.

        :param x: float x-coordinate
        :param y: float y-coordinate
        """
        self.move(x, y)

    def move(self, x: float, y: float) -> None:
        """
        Move the point to a new location in 2D space.

        :param x: float x-coordinate
        :param y: float y-coordinate
        """
        self.x = x
        self.y = y

    def reset(self) -> None:
        """
        Reset the point back to the geometric origin: 0, 0
        """
        self.move(0, 0)

    def calculate_distance(self, other: "Point") -> float:
        """
        Calculate the Euclidean distance from this point
        to a second point passed as a parameter.

        :param other: Point instance
        :return: float distance
        """
        return math.hypot(self.x - other.x, self.y - other.y)
# enter `help(Point)<enter>` at the Python prompt
print(help(Point))
