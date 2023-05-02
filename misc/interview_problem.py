
def chain_sum(number):
    result = number
    def wrapper(number2=None):
        nonlocal result
        if number2 is None:
            return result
        result += number2
        return wrapper
    return wrapper

# in python default recursion == 1_000
print(chain_sum(5)())  # 5
print(chain_sum(5)(2)())  # 7
print(chain_sum(5)(100)(-10)())  # 95


def chain_sum_without_if(number):
    result = number
    def wrapper(number2=None):
        nonlocal result
        try:
            number2 = int(number2)
        except TypeError:
            return result
        result += number2
        return wrapper
    return wrapper


def chain_sum_without_if_and_tryexcept(number):
    def wrapper(number2=None):
        def inner():
            wrapper.result += number2
            return wrapper
        logic = {
            type(None): lambda: wrapper.result,
            int: inner
        }
        return logic[type(number2)]()
    wrapper.result = number
    return wrapper


class ChainSum:
    def __init__(self, number):
        self._number = number

    def __call__(self, value=0):
        return ChainSum(self._number + value)

    def __str__(self):
        return str(self._number)
