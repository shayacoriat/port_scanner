"""port scanner run from the command line ,
 target ip as first sys.argv, 
 amount of ports to be scanned as the second 
sys.argv  

uses threading to speed up the process 
and queue's to ensure threads do not overlap """


import sys
import socket
import threading
from queue import Queue

host = sys.argv[1]
amount = int(sys.argv[2])
q = Queue()


# create socket and attempt to connect 
def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(.3)
    result = s.connect_ex((host, port))
    if result == 0:
        print("port {} is open".format(port))

# hold range of ports to be scanned in a queue
def ports():
    for port in range(amount):
        q.put(port)

# access one port at a time so theads don't overlap
def worker():
    while not q.empty():
        port = q.get()
        scan(port)


ports()
for i in range(25):
    thread = threading.Thread(target = worker)
    thread.start()

