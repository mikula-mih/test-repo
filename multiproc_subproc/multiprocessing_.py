from __future__ import annotations

''' Unlocking your CPU cores in Python '''
# https://www.youtube.com/watch?v=X7vBbelRXn0

# There are three big contenders for how to deal with multiple tasks in Python:
# asyncio
#   - cooperative pausing/waiting (good for waiting r/w disk, network connection)
#   - good for IO bound
# threading
#   - python has `GIL` == Global Interpreter Lock
#   - non-cooperative pausing/interrupting
#   - good for IO bound
#   - good to do long-running ops w/o blocking
# multiprocessing
#
# Creating processes and communicating between them can be very expensive, so
# 1. use multi-processing to things that are already taking a long time;
# 2. trying to send or recieve smth across process boundaries that's not picklable
#   (threads share virtual memory so a variable that you create in one thread
#   can be accessed in another thread, processes on the other hand have their own
#   address space and do not share virtual memory; without specifically using
#   shared memory a process cannot access variable from another process, the way
#   multiprocessing gets around this is by serializing everything using pickle;
#   the using inter-process communication method like a pipe to send bytes from
#   one process to another)
# 3. trying to send to much data
#   (instead of sending data consider sending a message like a string that informs
#   other process how to create the data)
# 4. using multiprocessing when there's a lot of shared computation between tasks
# 5. not optimizing the chunk size
#   (instead of submitting each item as a separate task for the pool items are
#   split into chunks; when a worker grabs more work it grabs an entire chunk of
#   work; bigger chunks allow individual workers to have to take less trips back
#   to the pool to get more work however there's also a trade-off because a bigger
#   chunk means that you have to copy more items at once across process boundaries
#   this can potentially cause you to run out of memory if your chunk size is too
#   large; if you're running out of memory consider setting a smaller chunk size
#   and also using imap or imap_unordered;

import os.path
import random
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import numpy as np
import scipy.io.wavfile

# `Lock` is a parallel processing primitive that helps threads prevent themselves
# from accessing the same data at the same;

def gen_fake_data(filenames):
    print("generating fake data")
    try:
        os.mkdir("sounds")
    except FileExistsError:
        pass

    for filename in filenames:  # homework: convert this loop to pool too!
        if not os.path.exists(filename):
            print(f"creating {filename}")
            gen_wav_file(filename, frequency=440, duration=60.0 * 4)


def gen_wav_file(filename: str, frequency: float, duration: float):
    samplerate = 44100
    t = np.linspace(0., duration, int(duration * samplerate))
    data = np.sin(2. * np.pi * frequency * t) * 0.0
    scipy.io.wavfile.write(filename, samplerate, data.astype(np.float32))


def etl(filename: str) -> tuple[str, float]:
    # extract
    start_t = time.perf_counter()
    samplerate, data = scipy.io.wavfile.read(filename)

    # do some transform
    eps = .1
    data += np.random.normal(scale=eps, size=len(data))
    data = np.clip(data, -1.0, 1.0)

    # load (store new form)
    new_filename = filename.removesuffix(".wav") + "-transformed.wav"
    scipy.io.wavfile.write(new_filename, samplerate, data)
    end_t = time.perf_counter()

    return filename, end_t - start_t


# `ETL` == Extract Transform Load
def etl_demo():
    filenames = [f"sounds/example{n}.wav" for n in range(24)]
    start_t = time.perf_counter()

    print("starting etl")
    # for filename in filenames:
    #     _, duration = etl(filename)
    #     print(f"{filename} completed in {duration:.2f}s")

    # `Pool` object represents a process pool;
    with Pool() as pool:
        results = pool.imap_unordered(etl, filenames)

        for filename, duration in results:
            print(f"{filename} completed in {duration:.2f}s")

    end_t = time.perf_counter()
    total_duration = end_t -start_t
    print(f"etl took {total_duration:.2f}s total")


def run_normal(items, do_work):
    print("running normally on 1 cpu")
    start_t = time.perf_counter()
    results = list(map(do_work, items))
    end_t = time.perf_counter()
    wall_duration = end_t - start_t
    print(f"it took: {wall_duration:.2f}s")
    return results


def run_with_mp_map(items, do_work, processes=None, chunksize=None):
    print(f"running using multiprocessing with {processes=}, {chunksize=}")
    start_t = time.perf_counter()
    with Pool(processes=processes) as pool:
        results = pool.imap(do_work, items, chunksize=chunksize)
    end_t = time.perf_counter()
    wall_duration = end_t - start_t
    print(f"it took: {wall_duration:.2f}s")
    return results


def fib(n):
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def n_fibs(n):
    if n < 2:
        return [i for i in range(n)]
    fibs = [0, 1]
    a, b = 0, 1
    for _ in range(n - 2):
        a, b = b, a + b
        fibs.append(b)
    return fibs


def compare_mp_map_to_normal():
    items = list(range(10000))
    do_work = fib
    run_with_mp_map(items, do_work)

    print()
    run_normal(items, do_work)


def main():
    etl_demo()
    # compare_mp_map_to_normal()


if __name__ == '__main__':
    main()
