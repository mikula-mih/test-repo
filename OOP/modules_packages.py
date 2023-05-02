# A `package` is a collection of `modules` in a folder.
#  "flat is better than nested."
"""`Absolute imports`
specify the complete path to the module, function, or class we want to import.
>>> import ecommerce.products
>>> product = ecommerce.products.Product("name1")

>>> from ecommerce.products import Product
>>> product = Product("name2")

>>> from ecommerce import products
>>> product = products.Product("name3")
"""
# The import statements use the period operator to separate packages or modules.
# A package is a namespace that contains module names, much in the way an object
# is a namespace containing attribute names.
"""`Relative imports`
identify a class, function, or module as it is positioned relative to the
current module.

from .database import Database

# The period in front of database says use the database module inside the current package.

from ..database import Database
from ..contact.email import send_mail

# the __init__.py file that defines a directory as a package
the ecommerce/__init__.py file contained the following line:
from .database import db
"""
# generally prefix an internal attribute or method with an underscore character, _.

# to strongly suggest that outside objects don't access a property or method:
# prefix it with a double underscore, __.
# this will perform `name mangling` on the attribute in question.
# When we use a double underscore, the property is prefixed with _<classname>.
# name mangling does not guarantee privacy; it only strongly recommends it.
