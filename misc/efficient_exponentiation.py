


class  EfficientExponentiation:

    def __init__(self, step_limit: int = None):
        initial_chain: tuple[int, ...] = (1,)
        self._min_mult_chain: dict[int,  tuple[int, ...]] = {1: initial_chain}
        self._cached_chains: set[tuple[int, ...]] = {initial_chain}
        self._step: int = 0
        self._step_limit = step_limit

    def _compute_next_step(self) -> None:
        if self._step_limit is not None and self._step >= self._step_limit:
            raise ValueError("step limit")
        self._step += 1
        new_chains = set()
        for chain in self._cached_chains:
            right_summand = chain[-1]
            for left_summand in chain:
                new_computed_val = left_summand + right_summand
                new_computed = chain + (new_computed_val,)
                new_chains.add(new_computed)
                self._min_mult_chain.setdefault(new_computed_val, new_computed)
        self._cached_chains = new_chains

    def _step_until_n_computed(self, n: int) -> None:
        if n <= 0:
            raise ValueError("n must be positive")
        while n not in self._min_mult_chain:
            self._compute_next_step()

    def minimal_multiplication_chain(self, n: int) -> tuple[int, ...]:
        self._step_until_n_computed(n)
        return self._min_mult_chain[n]

    def minimum_multiplications(self, n: int) -> int:
        return len(self.minimal_multiplication_chain(n)) - 1


def pow_15_naive(x):
   pass


def pow_15_minimal(x):
    # (1 2 3 6 12 15)
    x2 = x * x
    x3 = x2 * x
    x6 = x3 * x3
    x12 = x6 * x6
    x15 = x12 * x3
    return x15


def main():
    import time
    start = time.perf_counter()
    end = 300
    exp = EfficientExponentiation(step_limit=11)
    for i in range(1, end + 1):
        print(exp.minimal_multiplication_chain(i))
    print(sum(exp.minimum_multiplications(i) for i in range(1, end + 1)))
    elapsed = time.perf_counter() - start
    print(f"finished in {elapsed:.02f}s")


if __name__ == '__main__':
    main()
