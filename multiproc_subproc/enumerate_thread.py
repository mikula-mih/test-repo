import threading
import time

# Thread(group-None, target=None, name=None, args=(), kwargs={})

class thread(threading.Thread):
    '''
    thread1 = thread("GFG", 1000)
    thread1.start()
    '''
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

        # helper function to execute the threads
    def run(self):
        print(str(self.thred_name) +" "+ str(self.thread_ID));

def display():
    print(threading.current_thread().name, "...started")
    time.sleep(3)
    print(threading.current_thread().name, "...ended")

t1=threading.Thread(target=display, name="ChildThread1")
t2=threading.Thread(target=display, name="ChildThread2")
t3=threading.Thread(target=display, name="ChildThread3")
t1.start()
t2.start()
t3.start()

l=enumerate()
for t in l:
    print("Thread Name:", t.name)

time.sleep(5)
l=enumerate()
for t in l:
    print("Thread Name:", t.name)
