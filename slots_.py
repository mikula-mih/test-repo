import pytest
import sys
import getsize

'''Slots'''
# primarily a tool for saving memory usage when you have a lot of very small objects;

class MyClass:
    __slots__ = 'x', 'y', 'z'

    def __init__(self):
        self.x = 0
        self.y = "hello"
        self.z = False

def normal_class_example():
    print('NORMAL CLASS EXAMPLE')

    class A:
        v = 42

        def __init__(self):
            self.x = 'hello'

    a = A()
    print(a.x)
    # __dict__ dictionary only contains instant attributes, but not class variable,
    # that are not initialized;
    print('a dict:', a.__dict__)

    print('a.x (looked up in a dict):', a.x)
    a.x = 'world'
    print('a.x (looked up in a dict):', a.x)

    print('a.v (not found in a, looked up in A)', a.v)

    with pytest.raised(AttributeError):
        a.y # we never defined y

    a.y = ':)'
    print('a.y', a.y)


def slots_class_example():
    print('SLOTS CLASS EXAMPLE')

    class A:
        __slots__ = ('x',)
        v = 42 # class variable, not an instance

        def __init__(self):
            self.x = 'hello'

    a = A()

    with pytest.raised(AttributeError):
        print('a dict:', a.__dict__) # nope! slotted classes don't have dicts by default

    print('a.x (looked up in slots):', a.x)
    a.x = 'world' # can still modify slotted variables just fine
    print('a.x (looked up in slots):', a.x)

    with pytest.raises(AttributeError):
        a.y = ':(' # can't set a value for y, it's not one of the slots

    A.y = ':S'
    print('a.y (not found in a, looked up in A)', a.y)


def why_use_slots_example():
    print('WHY USE SLOTS EXAMPLE')

    class A:
        def __init__(self):
            self.x = 42

    class B:
        __slots__ = ('x',)

        def __init__(self):
            self.x = 42

    print('size of A (not slotted) instance:', sys.getsizeof(A()))
    print('size of B (slotted) instance:', sys.getsizeof(B()))

    print('recursive size of A (not slotted) instance:', getsize(A()))
    print('recursive size of B (slotted) instance:', getsize(B()))
    print('size A / size B:', getsize(A()) / getsize(B()))


def why_really_use_slots_example():
    print('WHY REALLY USE SLOTS EXAMPLE')

    class A:
        def __init__(sefl):
            self.x = 42
            self.y = 42
            self.z = 42
            self.t = 42
            self.u = 42
            self.v = 42
            self.w = 42

    class B:
        __slots__ = 'x', 'y', 'z', 't', 'u', 'v', 'w'

        def __init__(self):
            self.x = 42
            self.y = 42
            self.z = 42
            self.t = 42
            self.u = 42
            self.v = 42
            self.w = 42

# A `slot` is really just a piece of memory that you use for storing a particular
# piece of data about the instance;

def slots_with_inheritance():
    print('SLOTS WITH INHERITANCE')

    class A:
        __slots__ = 'x', 'y', 'z'

    class B(A):
        pass

    b = B()
    print("b dict:", b.__dict__) # b will have a dict unless you also specify slots in B

    b.x = 10
    print("b dict:", b.__dict__) # slotted variables stored in slot, not dict

    class C(A):
        __slots__ = ('+',) # only specify additional slots

    c = C()
    c.x = 10
    c.t = 10


def slots_with_metaclass():
    print('SLOTS WITH METACLASS')

    with pytest.raises(TypeError):
        class Meta(type):
            __slots__ = 'a', 'b' # metaclasses can only use empty slots

    class Meta(type):
        __slots__ = () # ok


def slots_with_dict():
    class A:
        __slots__ = ('__dict__',) # dict but not weakref

    class B:
        __slots__ = ('__weakref__',) # weakref but not dict

    class C:
        __slots__ = () # neither weakref nor dict

    class D:
        pass # both weakref + dict

    class E:
        __slots__ = '__dict__', 'x', 'y' # has dict, but x, y will not be in dict


if __name__ == '__main__':
    # normal_class_example()
    # slots_class_example()
    # why_use_slots_example()
    why_really_use_slots_example()
