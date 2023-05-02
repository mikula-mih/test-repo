
# MOST DISLIKED DUNDER???

class WhichOne:
    def __new__(cls, *args, **kwargs):
        ...

    def __iadd__(self, other):
        ... # implements +=

    def __repr__(self):
        ...

    def __del__(self):
        print(f"{self.__class__.__name__}.__del__")


class A:
    def __delitem__(self, key):
        print(f"{self.__class__.__name__}.__delitem__")

    def __delattr__(self, item):
        print(f"{self.__class__.__name__}.__delattr__")

    def __del__(self):
        print(f"{self.__class__.__name__}.__del__")


def what_del_is_not():
    x = A()

    str(x) # x.__str__()
    repr(x) # x.__repr__()
    len(x) # x.__len__()
    del x # NOPE

    del x[0] # corresponds to __delitem__
    del x.a # __delattr__
    del x # does not call __del__

# there big difference between the object itself and name you assign to it
# Every object in Python has a reference count; How many thing are referencing
# that object; Keyword `del` just delete name -> reduces refCount by one;
# __del__ runs when refCount hits 0;

class B:
    def __del__(self):
        print("cleanup code?")

def del_may_never_be_called():
    x = A()
    y = A()
    x.children = [y] # reference cycle
    y.parent = x

# if __del__ is called at all, it might be called while the interpreter is
# shutting down
class DumpOnDel:
    def __del__(self):
        with open("out.json", "w") as f:
            json.dump("test", f)

# __del__ purposefully supports the idea of resurrecting the object that is
# about to be deleted;
global_x = None

class Bad:
    def __del__(self):
        global global_x
        print(f"{self.__class__.__name__}.__del__")
        global_x = self # increace refCount it will not be garbage collected


# this class makes a temporary directory, or it will be remove when garbage collected;
class TempDir:
    def __init__(self):
        self.name = tempfile.mkdtemp()
        self._finalizer = weakref.finalize(self, shutil.rmtree, self.name)

    def remove(self):
        self._finalizer()
        # if self.name is not None:
        #     shutil.rmtree(self.name)
        #     self.name = None

    @property
    def removed(self):
        return not self._finalizer.alive
        # return self.name is None

    def __del__(self):
        self.remove()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove()

def best_del_alternative():
    with TempDir() as d:
        ...
    assert d.removed
