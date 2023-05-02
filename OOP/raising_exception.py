# Exceptions are raised, and interrupt the sequential execution of statements
# In Python, the exception that's raised is also an object.
# exception class inherit from a built-in class: `BaseException`
from typing import List

class EvenOnly(List[int]):
    def append(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Only integers can be added")
        if value % 2 != 0:
            raise ValueError("Only even numbers can be added")
        super().append(value)
# effects of an exception
from typing import NoReturn

def never_returns() -> NoReturn:
    print("I am about to raise an exception")
    raise Exception("This is always raised")
    print("This line will never execute")
    return "I won't be returned"
# a `traceback` shows the call stack
def call_exceptor() -> None:
    print("call_exceptor starts here...")
    never_returns()
    print("an exception was raised...so this line don't run")


""" Handling exceptions """
# by wrapping any code that might throw one inside a `try...except clause`
def handler() -> None:
    try:
        never_returns()
        print("Never executed")
    except Exception as ex:
        print(f"I caught an exception: {ex!r}")
    print("Executed after the exception")

from typing import Union
# the `raise` keyword, with no arguments, will re-raise the last exception if
# we're already inside an exception handler
def funny_division(divisor: float) -> Union[str, float]:
    try:
        if divisor == 13:
            raise ValueError("13 is an unlucky number")
        return 100 / divisor
    except (ZeroDivisionError, TypeError):
        return "Enter a number other than zero"
    except ValueError:
        print("No, No, not 13!")
        raise
#
some_exceptions = [ValueError, TypeError, IndexError, None]

for choice in some_exceptions:
    try:
        print(f"\nRaising {choice})
        if choice:
            raise choice("An error")
        else:
            print("no exception raised")
    except ValueError:
        print("Caught a ValueError")
    except TypeError:
        print("Caught a TypeError")
    except Exception as e:
        print(f"Caught some other error: {e.__class__.__name__}")
    else:
        print("This code called if there is no exception")
    finally:
        print("This cleanup code is always called")

""" the Exception hierarchy """
# most exceptions are subclasses of the Exception class
# exceptions must extend the BaseException class or one of its subclasses
""" BaseException: SystemExit, KeyboardInterrupt, Exception """
# to catch all exceptions (other than SystemExit and KeyboardInterrupt),
# always explicitly catch Exception
""" Defining our own exceptions """
from decimal import Decimal
# the Exception.__init__() method is designed to accept any arguments and store
# them as a tuple in an attribute named `args`
class InvalidWithdrawal(ValueError):
    def __init__(self, balance: Decimal, amount: Decimal) -> None:
        super().__init__(f"account doesn't have ${amount}")
        self.amount = amount
        self.balance = balance
    def overage(self) -> Decimal:
        return self.amount - self.balance

try:
    balance = Decimal('25.00')
    raise InvalidWithdrawal(balance, Decimal('50.00'))
except InvalidWithdrawal as ex:
    print("I'm sorry, but your withdrawal is "
            "more than your balance by "
            f"${ex.overage()}")
#
def divide_with_exception(dividend: int, divisor: int) -> None:
    try:
        print(f"{dividend  / divisor=}")
    except ZeroDivisionError:
        print("You can't divide by zero")

def divide_with_if(dividend: int, divisor: int) -> None:
    if divisor == 0:
        print("You can't divide by zero")
    else:
        print(f"{dividend  / divisor=}")
# `It's Easier to Ask Forgiveness Than Permission`: `EAFP`
# `Look Before You Leap`: `LBYL` - is less popular
# Exception syntax can be effective for `flow control`. Like an `if` statement,
# exceptions can be used for decision making, branching, and message passing.
