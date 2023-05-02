import prime_cython
import time


start_vanilla = time.time()
prime_cython.prime_finder_vanilla(4000)
end_vanilla = time.time()

print(end_vanilla - start_vanilla)

start_c = time.time()
prime_cython.prime_finder_optimized(4000)
end_c = time.time()

print(end_c - start_c)
