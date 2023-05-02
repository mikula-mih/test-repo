
""" Descriptors """
# object is a `descriptor` if it has any of these dunder methods (get,set,delete);
# and their purpose is to allow you to customize what it means to get, set, or
# delete an attribute;

class Descriptor:
    # defined per attribute
    # attribute itself that determines how it's accessed
    def __get__(self, obj, objtype=None):
        ...

    def __set__(self, obj, value):
        ...

    def __delete__(self, obj):
        ...


class SomeClass:
    x = Descriptor()

    # these defined per class
    # determines how to access attributes
    def __getattr__(self, item):
        ...

    def __setattr__(self, key, value):
        ...

    def __delattr__(self, item):
        ...


def what_are_descriptors():
    obj = SomeClass()

    print(obj.x)
    print(SomeClass.x)

    obj.x = 42
    del obj.x


# Descriptors
# 1. functions
class A:
    # every function you define def keyword is a descriptor that defines
    # a get method
    def f(self):
        pass

def functions():
    a = A()
    print(a.f) # access function through an instance -> get bound method
    print(A.f) # through class itself -> get function object


class Function:
    # ... other function stuff
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self # func itself
        return ... # bound func thingy


# 2. properties
class Rect:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    # area = property(area)
    # exectly the same as this:
    @property
    def area(self):
        return self.width * self.height


def properties():
    print(Rect.__dict__["area"])
    rect = Rect(2, 4)
    print(rect.area)


# 3. classmethods and staticmethods
class Animal:
    @classmethod
    def create(cls):
        return cls()

    @staticmethod
    def something_static():
        ...

def static_and_class_methods():
    animal = Animal.create()
    other = animal.create() # weird but ok


class ClassMethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)
        return self.f.__get__(objtype, objtype)

class StaticMethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f

# 4. slots
class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

keys = {
    "__get__",
    "__set__",
    "__delete__",
}

def slotted_variables():
    v = Vec3(0.0, 0.0, 0.0)
    v.x = 1.0 # ok
    # v.w = 1.0 # AttributeError
    m = Vec3.__dict__["x"]
    print(m)
    print(set(dir(m)) & keys)

# 5. __dict__
class E:
    pass

def dunder_dict():
    print(type(E.__dict__))
    obj = E.__dict__["__dict__"]
    print(obj)
    print(set(dir(obj)) & keys)

# 6. SQLAlchemy Models
Base = sqlalchemy.orm.declarative_base()

class User(Base):
    __tablename__ = "user_account"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                            primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

def sqlalchemy_models():
    m = User.__dict__["id"]
    print(m)
    user = User(id=0, name="James")
    print(user.name)

# 7. Validators

class GreaterThan:
    def __init__(self, val):
        self.val = val

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not value > self.val:
            raise ValueError(f"value must be greater than {self.val}")
        setattr(obj, self.name, value)

@dataclasses.dataclass
class Item:
    name: str
    price: float = GreaterThan(0.0)
    quantity: int = GreaterThan(0)

def field_validation():
    apple = Item("Apple", 1.50)
    # apple = Item("Apple", -1.50) # ValueError

# 8. super view lookups
def super_lookups():
    class Package:
        def ship(self, address):
            print("taking my time ...")

    class ExpressPackage(Package):
        def ship(self, address):
            print("on the way!")

    base_view = super(ExpressPackage)
    ExpressPackage.base_view = base_view

    ExpressPackage().ship(...)
    ExpressPackage().base_view.ship(...)


class NoisyDescriptor:
    def __get__(self, obj, objtype=None):
        print("get")

    def __set__(self, obj, value):
        print("set")

    def __delete__(self, obj):
        print("delete")


class MyClass:
    x = NoisyDescriptor()

    def __getattribute__(self, item): # always called
        print("getattribute")
        return object.__getattribute__(self, item) # implements descriptor logic

    def __getattr__(self, item): # called if __getattribute__ raises AttributeError
        print("getattr")

    def __setattr__(self, key, value): # always called
        print("setattr")
        object.__setattr__(self, key, value) # implements descriptor logic

    def __delattr__(self, item): # always called
        print("delattr")
        object.__delattr__(self, item) # implements descriptor logic


class DataDesc:
    def __get__(self, obj, objtype=None):
        ...

    def __set__(self, obj, value):
        ...

class NonDataDesc:
    def __get__(self, obj, objtype=None):
        ...

class Gotcha:
    x = DataDesc()
    y = NonDataDesc()

def gotchas_data_vs_nondata_descriptors():
    g = Gotcha()
    print(g.x, g.y) # None None
    g.__dict__["x"] = 42
    g.__dict__["y"] = 42
    print(g.x, g.y) # None 42
