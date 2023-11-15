from multiprocessing.connection import Listener, Client
from multiprocessing import Process
import threading
import mok_vars as v
import socket
from contextlib import closing
import hashlib

clientcon = False

def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def write_port(p):
    f = open(".ipcport", "w")
    f.write(str(p))
    f.close()

def read_port():
    f = open(".ipcport", "r")
    return int(f.read())

def MessageReceived(conn):
    msg = ''
    while True:
        try:
            msg = conn.recv()
            print(msg)
        except:
            conn.close()
            break

def listen():
    newport = get_free_port()
    write_port(newport)

    address = ('localhost', read_port())     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=str.encode(str(hashlib.sha256(v.paths.script.encode('utf-8')).hexdigest())))
    while True:
        threading.Thread(target=MessageReceived, args=(listener.accept(),)).start()
    listener.close()

def send(data):
    try:
        address = ('localhost', read_port())
        clientcon = Client(address, authkey=str.encode(str(hashlib.sha256(v.paths.script.encode('utf-8')).hexdigest())))
        clientcon.send(data)
        clientcon.close()        
    except:
        print("Mok not running? Start mok master first.")
        