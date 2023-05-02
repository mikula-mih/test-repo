
"""Object-Oriented Programming in Python"""
# Objects usually will have some state and some related behavior
# In Python we use the term "attribute" to identify both fields(state) and
# methods(behavior);
# the class is like a template to create an object
# objects ate also called instances of the class
# One difference berween the objects in Python and many other languages is that
# Python doesn't have private fields; In many other languages, the fields that
# we use to represent the internal state of the object will be private unless
# you explicitly make them public; The only way to access or modify the state
# will be using the methods; In Python we can do that directly;
# To indicate that a field is private prefix the name with an underscore
class Bicycle:
    def __init__(self):
        self._gear = 0
        self.__speed = 10
#
b = Bicycle()
print(b.__dict__) # {'_gear': 0, '_Bicycle__speed': 10}
#
# One of the purpose of writing funciton is to have a logical grouping of the code;
# When we need to keep track of a "state", we use classes, so that eack instance
# or object created from the class will have its own state;
# The methods you defined the class can be thought of as the behavior of these objects;
#
#
"""class & instance dictionaries in Python |__dict__|OOP"""
# classes have a __dict__ attribute
# it's a mapping proxy object - a read-only dictionary
class MyClass:
    pass
# >>> MyClass.__dict__
'''
mappingproxy({
    '__module__': '__main__',
    '__dict__': <attribute
        '__dict__' of 'MyClass' objects>,
    '__weakref__': <attribute
        '__weakref__' of 'MyClass' objects>,
    '__doc__': None,
})
'''
# Everything is an object in Python
# Classes are objects that allow us to create new objects or instances of the
# class;
# The __dict__ is used to store the attributes of the class
class MyClass:
    '''doc for MyClass'''
    a = 10
# >>> MyClass.__dict__
'''
mappingproxy({
    '__module__': '__main__',
    '__doc__': 'doc for MyClass',
    'a': 10,
    '__dict__': <attribute
        '__dict__' of 'MyClass' objects>,
    '__weakref__': <attribute
        '__weakref__' of 'MyClass' objects>,
    '__doc__': None,
})
'''
# >>> MyClass.__dict__['a']
# 10
# >>> MyClass.__dict__['a'] = 20
# TypeError: 'mappingproxy' object does not support item assignment
# >>> MyClass.__doc__
# >>> doc for MyClass
#
# Not all class attributes are stored in __dict__. For example, __name__;
# >>> MyClass.__name__
# >>> 'MyClass'
#
# the "dot" syntax
# to access the attributes of a class or object
MyClass.b = 30 # "dot" syntax also used for setting attibutes on classes
# these attributes will be stored in the class dictionary
# We can't set attributes on built-in classes like string or int;
# the convention is to name classes with camelcase starting with a capital letter;
# only classes that are written in C language like "str" or "int" will be
# with lowercase letters;
#
# There is a built-in function "vars" which will return the __dict__ of an object
# >>> vars(MyClass) # mappingproxy(...)
#
# Another way to access an attribute of a class or an object is using the built-in
# "getter" function
getattr(MyClass, 'a')
MyClass.a
# if you try to access an attribute that doesn't exist, "getattr" raises
# AttributeErro exception;
setattr(MyClass, 'a', 10)
delattr(MyClass, 'a') # same as >>> del MyClass.a
#
fields = {'a': 10, 'b': 20, 'c': 30}
for attr, val in fields.items():
    setattr(MyClass, attr, val)
print(MyClass.__dict__)
#
# the object also has its dictionary and we can access it using its __dict__ attribute;
obj = MyClass()
print(obj.__dict__) # {}
# Unlike class, an object's __dict__ is not a mappingproxy, but a normal dictionary;
# Since object dictionary is not read-only like class's dictionary, we can
# even assign attributes directly;
obj.__dict__['c'] = 30
print(getattr(obj, 'c'))
print(obj.__dict__)
#
# You can not modify the class attributes through objects directly;
# another thing to understand is the order of the attribute lookup:
# Python first checks in the object's dictionary, if the attribute is not there,
# then only Python will look in the class;
# The class attributes are shared across all the instances of that class;
# Things stored in the instance's dictionary are specific to that instance;
#
#
"""Instance Methods & self"""
# functions - callable attributes
# Declaring a class creates its namespace, so whatever attributes you define
# inside a class, can not be accessed directly outside the class;
# When we call the function using parentheses, a new object is created in memory,
# an instance of the class; The variable name will be a pointer or reference to
# that object; Just like all functions, our function also has its own scope; It
# doesn't have any access to the instance we created since it was defined outside
# its function body;
# When we call a function that is defined as a class attribute through an instance,
# Python automatically passes a reference to the same instance as the first argument,
# to the function; we should specify a parameter name in the definition of the
# function (def funct(self):) to capture this automatically passed reference to the object;
# >>> MyClass.say_hello
# <function __main__.MyClass.say_hello(self)>
# >>> obj = MyClass()
# >>> obj.say_hello
# <bound method MyClass.say_hello of
# <__main.MyClass object at 0x00000000000>>
# Memory address is that of the instance using which we called the method;
# Method is bound to that instance, So essentially, it's like calling the function
# in class and passing the object;
import types
# The actual types are defined in the "types" module
# The type of a function is "FunctionType" and that of a bound methods is "MethodType"
# >>> type(MyClass.say_hello) is types.Function
# The purpose of automatically injecting bound objects is to provide the method
# a handle to the object's namespace;
#
#
"""Instance Initializer __init__ method"""
# "self" is the reference to the object from which this method will be called
obj = MyClass()
# this created __dict__ in Heap memory; The __dict__ attribute of this object
# will be pointing to it's instance dictionary
#
# The purpose of __init__ is to initialize an object; it is not a constructor;
# Initializing an object means, populating its instance dictionary;
#
#
"""classmethod and staticmethod"""
# A method is implicitly passed the object on which it was called, for this reason,
# we use self as the first parameter in the definition of methods;
# The purpose of the "self" reference is to access the object's attribute, that is,
# whatever values are stored in its instance dictionary;
#
# Python provides ways to let it know that a function we defined inside a class
# doesn't have to be bound to its instance. Insted, we can tell Python to bind
# a method directly to the class;
# the "classmethod" decorator
# |=> the method will always be bound to the class instead of the instance
# Unlike a normal method, the class method can be called through either class
# or instance;
class MyClass:
    @classmethod
    def hello(cls):
        print(f'Hello from {cls}')
# The use of instance methods won't work if we wanted to modify a class attribute
# through its instances;
class Logger:
    enable_debug = False

    def print(self, msg):
        if self.enable_debug:
            print(msg)

    def set_debug(self):
        self.enable_debug = True
# 'set_debug' any instance should be able to call this method, and since it's
# modifying a class attribute, all other instances should see the change;
Logger.enable_debug = False
# Even if we call the "set_debug" method through one instance, only that instance
# starts printing messages on subsequent uses of the "print" method;
def testing(param: int):
    print(f"\nTesting attempt: {param}")
    log1 = Logger()
    log2 = Logger()
    log1.print("hello 1")
    log2.print("hello 2")
    log1.set_debug()
    log1.print("hello 1") # TRUE
    log2.print("hello 2")
    print(log1.__dict__)
    print(log2.__dict__)
    print(Logger.enable_debug)
#
testing(1)
# Instead, we should make it a class method and modify the class attribute directly
class Logger:
    enable_debug = False

    @classmethod
    def print(cls, msg):
        if cls.enable_debug:
            print(msg)

    @classmethod
    def set_debug(cls):
        cls.enable_debug = True
#
testing(2)
# Another reason to create a class method is when you want ot return a new object
# of the same class;
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Square:
    def __init__(self, length):
        self.length = length

    @classmethod
    def from_rectangle(cls, rect):
        min_side = min(rect.length, rect.width)
        return cls(min_side) # Square(min_side)
#
r = Rectangle(5, 10)
s = Square.from_rectangle(r)
print(f'\n {s.length} \n')
# A static method is never bound to anything
#
#
"""property decorator"""
class Circle:
    def __init__(self, radius):
        if radius < 0:
            raise ValueError("radius must be non-negative")
        self._radius = radius

    def get_radius(self):
        return self._radius

    def set_radius(self, new_radius):
        if new_radius < 0:
            raise ValueError("radius must be non-negative")
        self._radius = new_radius
    # the actual value of radius is stored in the private attribute "_radius"
    # and this private attribute is stored in the instance dictionary
    radius = property(fget=get_radius, fset=set_radius)
    # this "radius" attribute is a "property" object and it is stored in the
    # class dictionary;
# you have to use function calls to access the attribute;
# it's not as convenient as directly accessing the attributes, Python's solution
# to this problem is the "property" class;
#
# This is the signature of the property class's constructor
# class property(fget=None, fset=None, fdel=None, doc=None)
print(Circle.__dict__)
help(Circle) # will show docsting
print(property.__dict__)
#
class Circle:
    def __init__(self, radius):
        self._radius = radius

    def get_radius(self):
        return self._radius

    def set_radius(self, val):
        self._radius = val

    def del_radius(self):
        del self._radius

    radius = property(get_radius)
    radius = radius.setter(set_radius)
    radius = radius.deleter(del_radius)
# A decorator is just a fancy syntax for a function that accepts another function
# and returns a new one
# func = decorator(func) ==
# @decorator
# def func():
#   ...
import math

class Circle:
    def __init__(self, radius):
        self._radius = radius
        # a common pattern is to catch an error of computed attributes
        self._area = None

    @property
    def radius(self):
        """docstring"""
        return self._radius

    @property
    def area(self):
        if self._area is None:
            self._area = math.pi * (self._radius ** 2)
        return self._area

    @radius.setter
    def radius(self, val):
        self._radius = val
        self._area = None # invalidate the cache

    @radius.deleter
    def radius(self):
        del self._radius
#
c = Circle(5)
print(c.area)
#
#
"""Closures in Python"""
# Functions are first-class citizens in Python, and everything are objects;
def outer():
    a = 25
    name = "python"

    def inner(prefix):
        print(prefix, name)

    return inner # returning a reference to "inner" function object
# When Python sees the "def" statement for the "outer" function, a function object
# is created at some memory address and the name "outer" will be a reference to it;
# This function object will have attributes to store references to the objects that
# will be created when its body is executed; None of the objects inside its body is
# created yet;
my_func = outer()
my_func('prefix')
#
def counter(start):
    def inc1(step=1):
        nonlocal start
        start += step
        print(start)

    def inc2(step=1):
        nonlocal start
        start += step
        print(start)

    return inc1, inc2

my_inc, another_inc = counter(5)
my_inc() # 6
another_inc() # 7
my_inc() # 8
# both variables point to the same object because of the use of the "nonlocal"
# keyword; To achieve this, Python uses a cell object, Instead of pointing the "start"
# variable from both scopes to the free variable directly, an intermediary cell object
# is created at some memory address; This cell object stores the memory address of the
# actual free variable object; Whenever you modify a free variable, an object corresponding
# to the new value is created somewhere else in the memory, and its memory address is updated
# in the cell object;
print(my_inc.__code__.co_freevars)
# The "co_freevars" attribute returns a tuple of free variables the funciton references;
print(my_inc.__closure__)
# The "__closure__" attribute returns a tuple of cell objects that corresponds to
# each free variable;
print(my_inc.__closure__[0].cell_contents)
# use the "cell_contents" attribute of the cell object to see the current value of
# the free variable;
print(my_inc.__code__.co_varnames)
print(my_inc.__code__.co_cellvars)
# The "co_varnames" attribute shows a function's local variables and the "co_cellvars"
# attribute shows the names of local variables that are referenced by nested functions;
#
#
"""Variable Scopes & Namespaces - global/local/nonlocal"""
# The portion of the code where a variable is defined is called the lexical scope
# of the variable; The global scope is essentially the module scope, which means
# it spans a single file only; If you import another module, it will have its global
# scope; Each function has its local scope; Every time the function is called, a new
# scope is created; "print" is in Build-in scope;
# The variables or name bindings are stored in namespaces;
# Namespaces can be thought of as a table of labels to object references it is pointing to;
# The namespaces of global and local scopes are implemented using dictionaries;
a = 35
# Global keyword tells Python that a variable is meant to be scoped in the global scope
print(f'\nGlobal variables:\n{globals()}')
print(globals()['a'])
# to execute a function object use parenthesis and pass the argument
globals()['my_func']('globaly executed')
# Similarly, you can use the 'locals' function inside your function to get the
# dictionary that acts as its local namespace;
def new_func(input_var):
    local_var = "some str"
    print(locals())

new_func('var_str')
# Although local varibales are determined at the time when Python sees the 'def'
# statement, their values are only evaluated when you execute the function;
# The exception for this is if you define default values for parameters in the
# function signature;
a = 35
def outer():
    x = 25
    def inner():
        nonlocal x

# Using the 'nonlocal' keyword, we explicitly tell Python that we are modifying
# a non-local variable;
'''
def outer():
    global a
    a = 500
    def inner1():
        def inner2():
            nonlocal a # SyntaxError: no binding for nonlocal 'a' found
            a = 1
'''
# Chaining to the global namespace is not possible;
#
#
"""Variables in Python"""
# CPython - the reference Python interpreter written in C language;
# PyObject represents the base structure for all Python objects;
x = 543
# PyObject
# Type: Integer
# RefCount: 1
# Value: 543
# When you assign some value to a variable a new object is created in the heap memory;
# Python's memory manager periodically cleans objects with zero reference counts;
# This process is called garbage collection;
# Python is a dynamically typed language; Dynamic typing means that runtime objects or
# values have a type as opposed to static typing where variables have a type
# When you delete a variable, the actual object is not removed only the reference is
# removed and the reference count field of the object is decremented;
x = [865, 751, 932]
# PyVarObject
# Type: List
# RefCount: 1
# Value: )x1906
# Size: 3
# the "value" field will be a pointer to the memory location  of the storage array
# where actual elements are stored; Elements are not directly stored in this array;
# only pointers to the elements are stored;
# the basic structure for container type objects is PyVarObject;
xNone = None
yNone = None
print(hex(id(xNone)), hex(id(yNone)))
assert xNone is None
# `Interning` or re-using objects;
# At start, python pre-loads or caches a few the most commonly used objects so that
# it doesn't have to re-create them when needed;
# Integers in the inclusive range -5 to 256 are also interned;
#
# Python has two ways to check equality of two objects: "==" and "is"
#
# `Default Mutable Parameters`
# function objects has a '__defaults__' attribute which stores the default
# values as a tuple;
# The `+=` operator
old_list = [1, 2]
x_copy = old_list # same ids - same object
new_list = old_list + [3, 4] # creates new object
x_copy += [3, 4] # += operator calls the __iadd__ method of the object,-> python
# automatically passes 'self' as the first argument;
#
# You can modify a tuple using .append(), because a new tuple is created; but you
# can't assign tuple[0] = [num] to tuple because it uses pointers to memomry address,
# to an object that is immutable;
t = 1, [2, 3, 10]
# t[1] += [11, 12] # TypeError, but tuple is modified!!!!
# Since right hand side is evaluated first, the list gets modified;
#
#
""" Import System in Python
Module object
Regular_Namespace
Packages Finders
Loaders Relative imports
"""
# Importing the module creates does two things mainly: first, it creates a module
# object somewhere in the memory; then the module name is saved as a key in the
# current module's namespace dictionary;
# The value corresponding to this module name will be the address of the new
# module object;
# The module objects are instances of the "ModuleType" calss defined in the 'types' module;
import args_
import types
print(
    '\nImport System in Python\n',
    type(args_),
    isinstance(args_, types.ModuleType),
    hex(id(args_))
)
# we can even create a new module object ourselves by passing the module name and
# a docstring to 'ModuleType'
mod = types.ModuleType(
        'mod',
        'This is a test module'
)
print(mod)
# Like other variables, you can also create an alias to the module object
my_mod = args_
print(hex(id(my_mod)), hex(id(args_)))
# Both 'my_mod' and 'args_' will be regerences to the same object in memory;
# The import statement itself supports creating custom names for the module;
print(dir(args_))
# All the variables and functions that we declare at the global scope within 'args_'
# are available as module object attributes after the import;
# Python also creates a few other variables like '__file__', '__name__', etc...
print(args_.__dict__)
# All such symbols are stored in a dictionary of the 'args_' object;
print(args_.__name__)
# The '__name__' attribute will have the module name as its value
# The '__file__' attribute will have the absolute path of the module file
import sys
# Python exposes its import system through the 'meta_path' attribute of the 'sys' module;
print(sys.meta_path)
# Python's import system has two conceptual objects called finder and loader;
# a finder's  job is to locate a module and a loader's job is to load that module;
# find_spec(fullname, path, target=None)
# load_module(fullname)
# In practice, a finder is a class that has an instance method 'find_spec',
# and a loader is a class that has a 'load_module' instance method;
# What 'meta_path' shows is a list of finders;
# Some objects implement both 'finder' and 'loader' - an 'importer';
#
# Built-in modules are modules that are compiled into the Python interpreter
print(sys.builtin_module_names)
# The 'builtin_module_names' attribute of the 'sys' module returns a tuple of all
# such built-in module names;
#
# When Python executes the `import` statement, it first checks in a global cache
# of already loaded modules;
# This cache is just a dictionary with the module name as keys and module object
# as values;
# If the module is present in this cache, it's returned immediately; If not, Python's
# import protocol is invoked involving 'finders' and 'loaders';
# The 'loader' creates the module object in memory, then an entry is added to the
# global cache;
# `sys.modules` is the dictionary that maps the module names to modules that have
# already been loaded
# then in our current module's namespace, we get the name 'args_' as a reference to
# the module object
# print(globals())
del args_
print('Checking for module `args_`: ', 'args_' in globals()) # deleted from global namespace
# but the module object and its entry in 'sys.modules' persist
print('Checking for module `args_` in sys.modules: ', 'args_' in sys.modules)
# Deleting module simply removes the reference in our global namespace
del sys.modules['args_']
print('Deleted from sys.modules: ', 'args_' in sys.modules)
# !!!! it still just deletes the reference not the actual object
# there is one problem with importing module again, if some other module in our
# project had imported the module, they will have old module reference
import args_
# for such use cases use the 'reload' function provided by the 'importlib' module
# import importlib
# importlib.reload(args_)
print('Checking for module `args_` again: ', 'args_' in globals())
# if you import the module again, the module code is not compiled and excuted again,
# you get the reference to the existing module object;
#
# if there is an entry in 'sys.modules', no further checks are performed
sys.modules['my_test'] = lambda : print('hello')
# if we try to import it, it complits successfully;
import my_test
print(type(my_test))
my_test()
#
# Compile and Execute the source code ourselves
import sys
import types

module_name = "my_custom_module"
module_file = "./args_.py"

mod = types.ModuleType(module_name)
mod.__file__ = module_file

# set ref in sys.modules
sys.modules[module_name] = mod

with open(module_file, "r") as code_file:
    source_code = code_file.read()

# compile source code and create code object
code = compile(
    source_code,
    filename=module_file,
    mode="exec"
)

# execute compiled code. we need to specify
# a dictionary to store its global namespace
exec(code, mod.__dict__)
#
import socket as my_socket
# Some people use the 'from <module> import <symbol>' syntax hoping that it only
# imports the module partially and thus gets some benefit on performance or memory
# saving; That's not true; In either case, Python will complile and execute the entire
# module;
from socket import gethostname # there is no partial loading, the whole module is loaded
# The only performance benefit of using the second style import is that
# 'socket.gethostname' requires one additional lookup in the dictionary of 'socket'
# module to get to the 'gethostname' function object;
from socket import *
# Using import this way will mask the function name from one of other modules;
#
# `Packages` are a way of structuring Python's module Namespaces;
# for a package, module object will have the __path__ attribute set to its
# directory in which the package code resides;
# for modules the __path__ is not set;
# Python has 2 types of packages: `regular packages` and `namespace packages`
# `Regular Packaage` in Python a directory with one __init__ file inside it; when
# you import a package, the code inside the __init__ file is executed automatically;
# Simply importing a package doesn't import the modules inside it
#
# import package1.package2.package3
# but you can import it in __init__ of package, granting access to modules inside
# without importing all internal packages;
#
# Python supports relative imports:
# from . import mod2
# from .. import mod1
# Single 'dot' means the current directory, two 'dots' means its parent directory,
# and so on;
# Another important thing is that relative imports can only be used inside packages;
#
# Python doesn't have the concept of private attributes;
# However, there are some mechanisms to control what symbols are exported from
# a module or package; these mechanisms only apply when the user imports a module
# using 'from module import *' syntax: any symbol that is prefixed with an underscore
# won't be exported;
# 2nd method:
# defining a __all__ variable
__all__ = ["Bicycle", "Circle"] # will only import these symbols in the user's module
# in __init__.py of the package:
# from .module1 import *
# __all__ = module1.__all__
#
# `Namespace Package`: (no __init__ file | empty package)
# for regular packages its value will be the path to the __init__.py file;
# you can have modules or even regular packages inside Namespace Packages;
# Python even supports loading packages and modules from zip files;
# >>> import sys
# >>> sys.path.append('./pkg1.zip')
# >>> import pkg1.pkg2
# to import a package inside a zip file, the absolute filesystem path of the zip
# file must be present inside the 'sys.path' list
# you can also use the 'PYTHONPATH' environment variable
# >>> PYTHONPATH=./pkg1.zip python
# >>> import sys
# >>> sys.path
# >>> import pkg1
# If you run the Python interpreter after setting this environment variable,
# those entries will be added to the 'sys.path';
#
# the Python interpreter also takes a `-m` option to specify a module name that
# we want to run, then, Python will search for that module's '.py' file in
# 'sys.path' and execute it;
# You can make a package executable by specifying a __main__.py file under its
# directory; if you specify the package name as value to the '-m' option,
# Python will execute the __main__.py inside it;
# you can have both __init__.py and __main__.py files inside the same package;
# this setup will allow you to import it as a regular package and also make it
# essentially a CLI application;
