from threading import *
import time

def display():
    print(current_thread().name, "...started")
    time.sleep(3)
    print(current_thread().getName(), "...ended")

print("The Number of active Threads:", active_count())
t1=Thread(target=display, name="ChildThread1")
t2=Thread(target=display, name="ChildThread2")
t3=Thread(target=display, name="ChildThread3")
t1.start()
t2.start()
t3.start()
print("The Number of active Threads:", active_count())
time.sleep(5)
print("The Number of active Threads:", active_count())

import threading
threading.get_ident()
threading.enumerate()
threading.main_thread()
threading.settrace(fun)
threading.setprofile(fun)
threading.stack_size([size])
threading.TIMEOUT_MAX

threading.getName()
threading.setName()
threading.isAlive()
threading.isDaemon()
threading.setDaemon(daemonic)
