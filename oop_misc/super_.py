import time

def separet_dicts_example():
    pass


class LoggingDict(dict):
    def __setitem__(self, key, value):
        print(f'Setting {key}: {value}')
        super().__setitem__(key, value)

    def __getitem__(self, item):
        print(f'Getting {item}')
        return super().__getitem__(item)

    def __delitem__(self, key):
        print(f'Deleting {key}')
        super().__delitem__(key)


def logging_dict_example():
    print("LOGGING DICT EXAMPLE")
    d = LoggingDict()
    d[0] = "subscribe"
    x = d[0]
    del d[0]
    print()


###
class Base:
    @classmethod
    def f(self, x):
        print("Base.f", self, x)

class Derived(Base):
    # @classmethod
    def f(self, x):
        print("Derived.f", self, x) # <__main__.Derived object at 0x0000000000000000>
        super().f(x) # <class '__main__.Derived'>
        print("Derived.f finished")

def basic_example():
    d = Derived()
    d.f(42)

# `super` does NOT call your parent
def super_does_not_access_parent():
    # Method Resolution Order (MRO)
    class Root:
        def f(self):
            print("Root.f", self)

    class A(Root):
        def f(self):
            print("A.f", self)
            super().f()

    class B(Root):
        def f(self):
            print("B.f", self)
            super().f()

    class C(A, B):
        def f(self):
            print("C.f", self)
            super().f()

    a = C()
    a.f()
    # b = B()
    # b.f()
    print(C.__mro__)
    # if python searches through all of MRO & still can findan attribute then
    # an AttributeError is raised
    print([cls.__name__ for cls in C.__mro__])

    '''
    Rules of hierarchy:
    - make a root of everything
    - all versions MUST use super
    - use a fixed argument signature
    '''

def the_properties_of_mro_you_should_care_about():
    # (object,)

    class A: # (A, object)
        pass

    class B: # (B, object)
        pass

    class C(A, B): # C < A < B
        pass
        # the third important property is that the MRO of a child must be
        # an extension of the MRO of each of its parents;
        # That means each parent's MRO is a subsequence of the child's;
    '''
    class D(A, C): # error
        pass
    '''

class ValidatedSet(set):
    def __init__(self, *args, validators=None, **kwargs):
        self.validators = list(validators) if validators is not None else []
        if args:
            (elements,) = args
            self.validate_many(elements)
        super().__init__(*args, **kwargs)

    def validate_one(self, element):
        pass

    def validate_many(self, elements):
        pass

    def add(self, element):
        self.validate_one(element)
        super().add(element)

    def is_int(x):
        return isinstance(x, int)

    def validate_set_example():
        print("VALIDATE SET EXAMPLE")
        ints = ValidatedSet([1, 2, 3], validators=[is_int])
        print(ints)
        print()


class ReducedSet(set):
    def __init__(self, *args, reducer=None, **kwargs):
        self.reducer = reducer
        if args:
            (elements,) = args
            if reducer is not None:
                args = (map(reducer, elements),)

        super().__init__(*args, **kwargs)

    def add(self, element):
        if self.reducer is not None:
            element = self.reducer(element)
        super().add(element)


class ModularSet(ValidatedSet, ReducedSet):
    def __init__(self, *args, n, **kwargs):
        def reduce_mod_n(x):
            return x % n

        super().__init__(*args, validators=[is_int], reducer=reduce_mod_n, **kwargs)

    def modular_set_example():
        print("MODULAR SET EXAMPLE")
        mod5 = ModularSet([0, 1, 2, 5, 10], n=5)
        print(mod5)
        print()


# the return value of a super call is an instance of a super class;
def what_is_noargs_super():
    class A:
        def f(self):
            print(f"called A.f, self is {self}")

    class B(A):
        def f(self):
            print(f"called B.f, self is {self}")
            # super returns a `proxy object`
            sup = super()
            print(type(sup), sup)
            sup.f()

    B().f()

def simple_proxy_example():
    class SimpleProxyObj:
        def __init__(self, obj):
            self.obj = obj

        def __getattr__(self, item): # called when you proxy.abc
            return getattr(self.obj, item)

    obj = [1, 2, 3]
    proxy = SimpleProxyObj(obj)
    proxy.append(4) # append forwarded to obj
    print(obj)
    print(proxy)
    assert obj == [1, 2, 3, 4]


def kinda_super_proxy_example():
    class KindaSuperProxyObj:
        def __init__(self, cls, obj):
            self.obj = obj
            self.cls = cls

        def __getattr__(self, item):
            attr = getattr(self.cls, item)
            if hasattr(type(attr), '__get__'):
                attr = attr.__get__(self.obj)
            return attr

    class A:
        def f(self):
            print("A")

    class B:
        def f(self):
            print("B")
            KindaSuperProxyObj(A, self).f()

    obj = B()
    obj.f()


import inspect
def print_callers_locals():
    frame = inspect.currentframe()
    caller_locals = frame.f_back.f_locals
    print(f"caller's locals: {caller_locals}")

def know_your_caller():
    x = 5
    s = "string"
    print_callers_locals()


def twoarg_super_can_be_used_anywhere():
    class A:
        def f(self):
            print(f"called A.f, self is {self}")

    class B(A):
        def f(self):
            print(f"called B.f, self is {self}")
            # two args from super()
            # super() is a proxy object that stores the class that it's
            # currently being run from & the object that it's currently being
            # run on; then it uses the MRO to find the next thing in line;
            super(__class__, self).f()


    b = B()
    sup = super(B, b)
    print("super(B, b)")

    print("super self", sup.__self__)
    print("super self class", sup.__self_class__)
    print("super thisclass", sup.__thisclass__)


# pure python implementation of super()
class Super():
    """
    A crazy implementation of the builtin super from within Python.
    Probably full of bugs, for instructional purposes only.
    """

    def __init__(self, cls=None, obj_or_cls=None, /):
        if cls is None and obj_or_cls is None:
            frame = inspect.currentframe()
            caller_locals = frame.f_back.f_locals
            assert frame.f_back.f_code.co_argcount > 0
            obj_or_cls = next(iter(caller_locals.values()))
            try:
                cls = caller_locals['__class__'] # depends on caller user __class__
            except KeyError:
                raise RuntimeError(
                    "For zero-argument Super, you need to put __class__ in the same function "
                    "that Super is used to make compiler magic work, the real super "
                    "doesn't have this restriction")

        assert inspect.isclass(cls), "cls must be a class"
        self.__thisclass__ = cls
        self._bind_self(cls, obj_or_cls)

    def _bind_self(self, cls, obj_or_cls, /):
        if obj_or_cls is None:
            self.__self__ = None
            self.__self_class__ = None
        elif inspect.isclass(obj_or_cls):
            assert issubclass(obj_or_cls, cls), "obj_or_cls is a class but not a subclass of cls"
            self.__self__ = obj_or_cls
            self.__self_class__ = obj_or_cls
        else:
            assert isinstance(obj_or_cls, cls), "obj_or_cls is an object but not an instance of cls"
            self.__self__ = obj_or_cls
            self.__self_class__ = type(obj_or_cls)

    def __get__(self, instance, owner=None):
        if self.__self__ is not None:
            return self
        if instance is not None:
            obj_or_cls = instance
        else:
            assert owner is not None, "cannot bind to None"
            obj_or_cls = owner

        self._bind_self(self.__self_class__, obj_or_cls)
        return self

    def __getattr__(self, item):
        if item == "__class__":
            return self.__class__

        if self.__self__ is None:
            raise AttributeError(item)

        mro = self.__self_class__.__mro__
        n = len(mro)
        i = mro.index(self.__thisclass__) + 1

        while i < n:
            cls = mro[i]
            try:
                res = cls.__dict__[item]
            except KeyError:
                pass
            else:
                try:
                    get = type(res).__get__ # get(self, instance, owner)
                except AttributeError:
                    return res
                else:
                    return get(res,
                                None if self.__self__ == self.__self_class__ else self.__self__,
                                self.__self_class__)

            i += 1
        raise AttributeError(item)


def main():

    class A:
        def f(self):
            return ["A"]

    class B(A):
        def f(self):
            __class__ # add __class__ to locals
            return ["B"] + Super().f()

    ###?

    class H(G):
        def f(self):
            __class__
            return ["H"] + Super().f()

    class H_super(G):
        def f(self):
            return ["H"] + Super().f()

    print(B().f())
    print(B_super().f())
    print(C().f())
    print(C_super().f())
    print(E().f())
    print(E_super().f())
    print(F().f())
    print(F_super().f())
    print(H().f())
    print(H_super().f())


# `super` means "next in line"
if __name__ == "__main__":
    print(time.ctime())
    basic_example()
    logging_dict_example()
    super_does_not_access_parent()
    print("\nWhat is noargs super():")
    what_is_noargs_super()
    print("\nsimple proxy example:")
    simple_proxy_example()
    print("\nkinda super proxy example:")
    kinda_super_proxy_example()
    # print_callers_locals()
    twoarg_super_can_be_used_anywhere()
