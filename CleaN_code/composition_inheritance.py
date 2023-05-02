
""" Composition and inheritance """
# polymorphism, inheritance, and encapsulation
#
# The proper way to reuse code is to have highly cohesive objects
# that can be easily composed and that could work on multiple contexts;
#
# The superclass is vaguely defined and contains too much responsibility,
# instead of a well-defined interface
# The subclass is not a proper specialization of the superclass it is trying to extend
#
# Anti-patterns for inheritance
#
# The correct use for inheritance is to specialize objects and create more
# detailed abstractions starting from base ones;
import collections
import datetime

class TransactionalPolicy(collections.UserDict):
    """Example of an incorrect use of inheritance."""

    def change_in_policy(self, customer_id, **new_policy_data):
        self[customer_id].update(**new_policy_data)

policy = TransactionalPolicy({
    "client001": {
        "fee": 1000.0,
        "expiration_date": datetime.datetime(2022, 1, 3),
    }
})
print(policy["client001"])
policy.change_in_policy("client001", expiration_date=datetime.datetime(2020, 1, 4))
print(policy["client001"])
print(dir(policy))
# This is a problem of mixing implementation objects with domain objects;
# A dictionary is an implementation object, a data structure, suitable for
# certain kinds of operation, and with a trade-off like all data structures;
#
# Implementation classes should be extending solely when creating other,
# more specific, implementation classes;
#
# the correct solution here is to use composition;
class TransactionalPolicy:
    """Example refactored to use composition."""

    def __init__(self, policy_data, **extra_data):
        self._data = {**policy_data, **extra_data}

    def change_in_policy(self, customer_id, **new_policy_data):
        self._data[customer_id].update(**new_policy_data)

    def __getitem__(self, customer_id):
        return self._data[customer_id]

    def __len__(self):
        return len(self._data)


""" Multiple inheritance """
# `Method Resolution Order (MRO)`
# `diamond problem`
class BaseModule:
    module_name = "top"

    def __init__(self, module_name):
        self.name = module_name

    def __str__(self):
        return f"{self.module_name}:{self.name}"

class BaseModule1(BaseModule):
    module_name = "module-1"

class BaseModule2(BaseModule):
    module_name = "module-2"

class BaseModule3(BaseModule):
    module_name = "module-3"

class ConcreteModuleA12(BaseModule1, BaseModule2):
    """Extend 1 & 2"""

class ConcreteModuleA23(BaseModule2, BaseModule3):
    """Extend 2 & 3"""

# There is no collision;
# Python resolves this by using an algorithm called `C3 linearization` or
# `MRO`, which defines a deterministic way in which methods are going to be called;
print(str(ConcreteModuleA12("test")))
# specifically ask the class for its resolution order
print(
    [cls.__name__ for cls in ConcreteModuleA23.mro()]
)

""" Mixins """
# a `mixin` is a base class that encapsulates some common behavior with the goal
# of reusing code;
class BaseTokenizer:

    def __init__(self, str_token):
        self.str_token = str_token

    def __iter__(self):
        yield from self.str_token.split("-")

tk = BaseTokenizer("28a2320b-fd3f-4627-9792-a2b38e3c46b0")
print(
    list(tk)
)

class UpperIterableMixin:
    def __init__(self):
        return map(str.upper, super().__iter__())

class Tokenizer(UpperIterableMixin, BaseTokenizer):
    pass
