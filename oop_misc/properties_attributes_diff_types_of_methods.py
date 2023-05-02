
""" Properties, attributes, and different types of
methods for objects """

class Connector:
    def __init__(self, source):
        self.source = source
        self._timeout = 'single ungerscore'
        self.__timeout = 60

    def connect(self):
        print("connecting with {0}s".format(self.__timeout))

conn = Connector("postgresql://localhost")
conn.connect()
print(f'{conn._timeout=}')
# will raise an AttributeError for conn.__timeout
# `name mangling` python creates a different name for the attribute with
# double underscore: _<class-name>__<attribute-name>
# using double underscore is considered non-Pythoic
print(f'{conn.source=}, {conn._Connector__timeout=}\n{conn.__dict__=}')

""" Properties """
import re

EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(potentially_valid_email: str):
    return re.match(EMAIL_FORMAT, potentially_valid_email) is not None

class User:
    def __init__(self, username):
        self.username = username
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not is_valid_email(new_email):
            raise ValueError(f"Can't set {new_email} as it's not a valid email")
        self._email = new_email


u1 = User("jsmith")

try:
    u1.email = "jsmith@"
except ValueError as e:
    print(e)

u1.email = "jsmith@g.co"
print(u1.email)
