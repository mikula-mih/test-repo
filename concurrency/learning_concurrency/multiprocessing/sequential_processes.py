
""" Communicating sequential processes """

""" PyCSP """
# python3.6 -m pip install pycsp

from pycsp.parallel import *
import time

@process
def Process1():
    time.sleep(1)
    print('process1 exiting')

@process
def Process2():
    time.sleep(1)
    print('process2 exiting')

Parallel(Process1(), Process2()) # Blocks
print('program terminating')
