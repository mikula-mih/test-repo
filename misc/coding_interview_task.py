
# 1
def chain_sum(number):
    result = number
    def wrapper(number2=None):
        nonlocal result
        if number2 is None:
            return result
        result += number2
        return wrapper
    return wrapper

class chain_sum:
    def __init__(self, number):
        self._number = number

    def __call__(self, value=0):
        return chain_sum(self._number + value)

    def __str__(self):
        return str(self._number)

class chain_sum(int):
    def __call__(self, addition=0):
        return chain_sum(self + addition)

print(
    chain_sum(5)() # 5
)
print(
    chain_sum(5)(2)() # 7
)
print(
    chain_sum(5)(100)(-10)() # 95
)

# 2 : functional

def _digit(number, operator=None):
    if operator is None:
        return number
    return operator(number)

def zero(operator=None): return _digit(0, operator)
def one(operator=None): return _digit(1, operator)
def two(operator=None): return _digit(2, operator)
def three(operator=None): return _digit(3, operator)
def four(operator=None): return _digit(4, operator)
def five(operator=None): return _digit(5, operator)
def six(operator=None): return _digit(6, operator)
def seven(operator=None): return _digit(7, operator)
def eight(operator=None): return _digit(8, operator)
def nine(operator=None): return _digit(9, operator)

def plus(second_operand):
    return lambda first_operand: first_operand + second_operand
def minus(second_operand):
    return lambda first_operand: first_operand - second_operand
def times(second_operand):
    return lambda first_operand: first_operand * second_operand
def divided_by(second_operand):
    return lambda first_operand: first_operand / second_operand

print(
    seven(times(five()))
) # 35
