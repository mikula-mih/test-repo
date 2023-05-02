

def slow_pow(x, n: int):
    res = 1
    for _ in range(n):
        res *= x
    return res


# EVEN: x ** n == (x ** (n // 2)) ** 2
# ODD: x ** n == x * (x ** (n // 2)) ** 2
def fast_pow(x, n: int):
    if n == 0:
        return 1
    half_n, remainder = divmod(n, 2) # n // 2, n % 2
    result = fast_pow(x, half_n)
    result *= result
    return x * result if remainder else result


def fast_pow_extra(mul, identity, x, n: int):
    if n == 0:
        return 1
    half_n, remainder = divmod(n, 2)
    result = fast_pow_extra(mul, identity, x, half_n)
    result = mul(result, result)
    return mul(x, result) if remainder else result



def int_examples():
    assert slow_pow(1, 100) == 1
    assert slow_pow(5, 3) == 125
    assert slow_pow(2, 11) == 2048
    # assert fast_pow(1, 100) == 1
    # assert fast_pow(5, 3) == 125
    # assert fast_pow(2, 11) == 2048

def main():
    int_examples()


if __name__ == '__main__':
    mul = lambda x, y: x * y
    identity = 1
    main()
