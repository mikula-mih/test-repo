
def get_values():
    yield "hello"
    yield "world"
    yield 123

def example_get_values():
    gen = get_values()
    print(gen)
    print(next(gen))
    print(next(gen))
    print(next(gen))

    for x in get_values():
        print(x)


class Range:
    def __init__(self, stop: int):
        self.start = 0
        self.stop = stop

    def __iter__(self) -> Iterator[int]:
        curr = self.start
        while curr < self.stop:
            yield curr
            curr += 1

# we can now iterate over our range just the way we would over build-in range;
# just like the built-in range because we're only storing the start and the
# stop, not all the numbers in between -> we can construct huge ranges
def range_example():
    for n in Range(1000000000000000000000):
        print(n)
        if n == 4: break

# another common use for generators is reading from a file
class MyDataPoint(NamedTuple):
    x: float
    y: float
    z: float

def mydata_reader(file):
    for row in file:
        cols = row.rstrip().split(",")
        cols = [float(c) for c in cols]
        yield MyDataPoint._make(cols)

def example_reader():
    with open("mydata.txt") as file:
        for row in mydata_reader(file):
            print(row)

# `Lazy sequences` & Collatz
# `The Collatz Conjecture`
def collatz(n):
    while True:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        yield n
        if n == 1:
            break

def example_collatz():
    n = 27
    seq = list(collatz(n))
    print(sum(1 for _ in collatz(n)))
    print(seq)

# defining a generator
def example_gen_comp():
    # list comprehension creates all elements in memory immediately
    squares = [x*x for x in range(5)]
    # this code will not be computed until you try to iterate over the generator
    squares = (x*x for x in range(5)) # generator comprehension
    sum_sqs = sum(x*x for x in range(5))

# generators are extremly easy to compose
def example_composable():
    with open("nums.txt") as file:
        nums = (row.partition("#")[0].rstrip() for row in file)
        nums = (row for row in nums if rows)
        nums = (float(row) for row in nums)
        nums = (x for x in nums if math.isfinite(x))
        nums = (max(0., x) for x in nums)
        s = sum(nums)
        print(f"the sum is {s}")

# generators are bi-directional pipelines
def worker(f):
    tasks = collections.deque()
    value = None
    while True:
        batch = yield value
        value = None
        if batch is not None:
            tasks.extend(batch)
        else:
            if tasks:
                args = tasks.popleft()
                value = f(*args)

def example_worker():
    w = worker(str)
    w.send(None)
    w.send([(1,), (2,), (3,)])
    print(next(w))
    print(next(w))
    print(next(w))
    w.send([(4,), (5,)])
    print(next(w))
    print(next(w))

def example_worker_2():
    w = worker(str)
    w.send(None)
    w.send([(1,), (2,), (3,)])
    # w.throw(ValueError)
    w.close()

# under the hood in Python async/await co-routines are defined in terms of
# generators
async def async_video_when():
    await asyncio.sleep(42)

# yield from allows one generator to yield values from another generator
def another_generator():
    # yield from (x*x for x in range(5))
    for sq in (x*x for x in range(5)):
        yield sq

def quiet_worker(f):
    while True:
        w = worker(f)
        try:
            # return_of_subgen = yield from w
            yield from w
        except Exception as exc:
            print(f"ignoring {exc.__class__.__name__})
