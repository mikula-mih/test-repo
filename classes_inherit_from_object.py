
# Why do some Python classes inherit from object?

class A:
    pass

class B():
    pass

# object = int
''' Yes. it will inherit from int '''
class C(object):    # introduced in 2.2
    pass


assert all(object in cls.__bases__ for cls in [A, B, C])


# new style classes added:
class D(object):
    # descriptor protocol
    @property
    def x(self):
        return ...
    # support for dunder __new__
    def __new__(cls, *args, **kwargs):
        return ...
    # method resolution order (MRO)
    def f(self):
        super(C, self).f()
