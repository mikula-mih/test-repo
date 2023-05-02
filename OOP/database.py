# from ecommerce.database import database
from typing import Optional


class Database:
    """The Database Implementation"""

    def __init__(self, connection: Optional[str] = None) -> None:
        """Create a connection to a database."""
        pass


database = Database("path/to/data")
# or we could delay creating the database until it is actually needed
db: Optional[Database] = None
# the Optional[Database] type hint signals to the mypy tool that this may be
# None or it may have an instance of the Database class.

def initialize_database(connection: Optional[str] = None) -> None:
    global db   # module-level variable, outside the function
    # local variable would be discarded when the function exits
    db = Database(connection)

def get_database(connection: Optional[str] = None) -> Database:
    global db
    if not db:
        db = Database(connection)
    return db

# Classes can be defined anywhere. They are typically defined at the module level,
# but they can also be defined inside a function or method, like this:
class Formatter:
    def format(self, string: str) -> str:
        pass

def format_string(string: str, formatter: Optional[Formatter] = None) -> None:
    """
    """

    class DefaultFormatter(Formatter):
        """Format a string in title case."""
        def format(self, string: str) -> str:
            return str(string).title()

    if not formatter:
        formatter = DefaultFormatter()

    return formatter.format(string)
