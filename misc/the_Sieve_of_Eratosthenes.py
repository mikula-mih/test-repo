
''' Finding Primes with the Sieve of Eratosthenes '''

from math import isqrt

def primes_less_then(n: int) -> list[int]:
    if n <= 2:
        return []
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, isqrt(n)+1):
        if is_prime[i]:
            for x in range(i*i, n, i):
                is_prime[x] = False

    return [i for i in range(n) if is_prime[i]]



def NEW(n: int) -> list[int]:
    if n <= 2:
        return []
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, isqrt(n)+1):
        if is_prime[i]:
            for x in range(i*i, n, i):
                is_prime[x] = False

    return [i for i in range(n) if is_prime[i]]


def test():
    import time

    start = time.perf_counter()
    print(len(primes_less_then(100 ** 9))) # should be 50,847,537 according to wikipedia
    elapsed = time.perf_counter() - start
    print(f'done in {elapsed:.2f}s')


if __name__ == '__main__':
    print(primes_less_then(1000))

'''
https://github.com/mCodingLLC/prime_sieve
'''
