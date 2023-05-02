

class A:
    def __new__(cls, *args, **kwargs):
        print('new', cls, args, kwargs)
        return super().__new__(cls) # must return the object

    def __init__(self, *args, **kwargs):
        print('init', self, args, kwargs) # just initializes values

# both __new__ and __init__ are part of constructing of an object
# both of them get called when you try to create an instance of a class
def how_object_construction_works():
    # __new__ method gets called with class A + args
    x = A(1, 2, 3, x=4)
    # whereas __init__ method gets passed an actual instance of the object + args

    # here what happens when you try to execute the above code
    # first the __new__ method is called
    x = A.__new__(A, *args, **kwargs)
    # then if the returned object has the correct type
    if isinstance(x, A):
        # it will go ahead an call the __init__ method
        type(x).__init__(x, *args, **kwargs)

# __new__ is responsible for creating and returning the actual object;
# __init__ is responsible for initializing it, setting default values and etc.
#
# __new__ is added into Python, primarily to allow programmers to subclass built-in
# immutable types;
class UppercaseTuple(tuple):
    def __new__(cls, iterable):
        upper_iterable = (s.upper() for s in iterable)
        return super().__new__(cls, upper_iterable)
        # it's only possible because we are modifying the arguments before
        # this immutable thing is actually created;
    '''
    def __init__(self, iterable):
        print(f'init {iterable}')
        for i, arg in enumerate(iterable):
            self[i] = arg.upper() # by the time the init is called its to late
            # the object already exists and it cannot be changed; the only
            # way to get around this is to intercept and modify the args before
            # the object is created
    '''

def inheriting_immutable_uppercase_tuple_example():
    print("UPPERCASE TUPLE EXAMPLE")
    print(UppercaseTuple(["hi", "there"]))

# Another interesting way __new__ can be used;
# Singleton design pattern -> the purpose of a singleton is that there's only
# supposed to be one of them; {global configuration object, that everything is
# supposed to share, you allways supposed to get the same instance: prevents
# everyone to get out of sync, they just all have a reference to the same object}
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


def singleton_example():
    print("SINGLETON EXAMPLE")
    x = Singleton()
    y = Singleton()
    print(f'{x is y=}')

# imagine having an object that is increadibly expansive to initialize;
# if that is the case, you definitly don't want to create a new instance if you
# already have one in memory;
class Client:
    _loaded = {}
    _db_file = "file.db"

    def __new__(cls, client_id):
        if (client := cls._loaded.get(client_id)) is not None:
            print(f'returning existing client {client_id} from cache')
            return client
        client = super().__new__(cls)
        cls._loaded[client_id] = client
        client._init_from_file(client_id, cls._db_file)
        return client

    def _init_from_file(self, client_id, file):
        # lookup client in file and read properties
        print(f'reading client {client_id} data from file, db, etc.')
        name = ...
        email = ...
        self.name = name
        self.email = email
        self.id = client_id

def cached_clients_example():
    print("CLIENT CACHE EXAMPLE")
    x = Client(0)
    y = Client(0)
    print(f'{x is y=}')
    z = Client(1)

# imagine we want an encrypted file class that's able to read encrypted files;
def encrypted_file_example():
    print("EMCRYPTED FILE EXAMPLE")
    print(EncryptedFile('plaintext_hello.txt').read())
    print(EncryptedFile('rot13:///rot13_hello.txt').read())
    print(EncryptedFile('opt:///opt_hello.txt', key='1234').read())
# we'll have different classes for different kinds of encryption;
class Plaintext(EncryptedFile, prefix='file'):
    # for a plain text file, we just open the file and return its contents;
    def read(self):
        with open(self.file, 'r') as f:
            return f.read()

class ROT13Text(EncryptedFile, prefix='rot13'):
    # read the file, and then decode it as ROT 13 and return that;
    def read(self):
        with open(self.file, 'r') as f:
            text = f.read()
        return codecs.decode(text, 'rot_13')

class OneTimePadXorText(EncryptedFile, prefix='opt'):
    def __init__(self, path, key):
        if isinstance(self.key, str):
            self.key = self.key.encode()

    def xor_bytes_with_key(self, b: bytes) -> bytes:
        return bytes(b1 ^ b2 for b1, b2 in zip(b, itertools.cycle(self.key)))

    def read(self):
        with open(self.file, 'rb') as f:
            btext = f.read()
        text = self.xor_bytes_with_key(btext).decode()
        return text


class EncryptedFile: #  DO NOT USE ANY OF THIS FOR REAL ENCRYPTION
    _registry = {} # rot13 -> ROT13Text

    def __init_subclass__(cls, prefix, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[prefix] = cls

    def __new__(cls, path: str, key=None):
        prefix, sep, suffix = path.partition(':///')
        if sep:
            file = suffix
        else:
            file = prefix
            prefix = "file"
        subclass = cls._registry[prefix]
        obj = object.__new__(subclass)
        obj.file = file
        obj.key = key
        return obj

    def read(self) -> str:
        raise NotImplementedError


class Drawable(ABC):

    @abstractmethod # marks draw with __isabstractmethod__ = True
    def draw(self):
        return NotImplemented
