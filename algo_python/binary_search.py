
""" Binary Search """
# also called `Bisection Search` is an algorithm for finding an element quickly
# in a sorted array;

# from bisect import bisect_left, bisect_right

def bisect(arr: list, x) -> int:
    lo = 0
    hi = len(arr)
    while lo < hi:
        mid = (lo + hi)//2  # lo + (hi-lo)//2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bisect_left(arr: list, x, lo=0, high=None) -> int:
    hi = hi if hi is not None else len(arr)
    assert 0 <= lo <= hi <= len(arr)
    while lo < hi:
        mid = (lo + hi)//2  # lo + (hi-lo)//2
        if arr[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def bisect_index_of(arr: list, x) -> lint:
    i = bisect_left(arr, x)
    if i != len(arr) and arr[i] == x:
        return i
    raise ValueError


def main():
    # [2, 3, 3, 4, 6, 7, 8, 9] # remaining: 8
    # [            6, 7, 8, 9] # remaining: 4
    # [            6, 7      ] # remaining: 2
    # [               7      ] # remaining: 1
    # logarithmic time complexity
    # N/2^k ~= 1 -> done, k = log_2(N)

    # i = bin_search([2, 3, 3, 4, 6, 7, 8, 9], 7)

if __name__ == '__main__':
    main()
