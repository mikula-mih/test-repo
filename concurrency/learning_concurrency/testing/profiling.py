
""" cProfile """
# python3.6 -m cProfile <file>.py
""" line_profiler tool """
# pip install line_profiler
""" Kernprof """
import random
import time

@profile
def slowFunction():
    time.sleep(random.randint(1, 5))
    print("Slow Funciton Executed")

def fastFunction():
    print("Fast Function Executed")

def main():
    slowFunction()
    fastFunction()

if __name__ == "__main__":
    main()
# python3.6 -m kernprof -l <file>.py
# result .lprof file
# python3.6 -m line_profiler <file>.py.lprof

""" Memory profiling """
# pip install -U memory_profiler
# python3.6 -m memory_profiler <file>.py

""" memory profile graphs """
# series of .dat files
# python -m pip install matplotlib
# mprof run <file>.py
# mprof plot
