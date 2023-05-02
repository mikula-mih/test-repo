
""" Listeners and clients """
# multiprocessing.connection module is a high-level message-oriented API for
# dealing with sockets or Windows named pipes;
from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000) # family is deduced to be 'AF_INET'
# Listener Class
with Listener(address, authkey=b'secret password') as listener:
    with listener.accept() as conn:
        print('connection accepted from', listener.last_accepted)

        conn.send([2.25, None, 'junk', float])

        conn.send_bytes(b'hello')

        conn.send_bytes(array('i', [42, 1729]))

# Client Class
from multiprocessing.connection import Client
from array import array

with Client(address, authkey=b'secret password') as conn:
    print(conn.recv()) # => [2.25, None, 'junk', float]

    print(conn.recv_bytes()) # => 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    print(conn.recv_bytes_into(arr)) # => 8
    print(arr) # => array('i', [42, 1729, 0, 0, 0])
