from multiprocessing.connection import Listener, Client
from multiprocessing import Process
import threading
import mok_vars as v
import socket
from contextlib import closing
import hashlib
import time
import sys

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
    threading.Thread(target=testsendinterval, args=(conn,)).start()

    msg = ''
    while True:
        try:
            msg = conn.recv()
            print(msg)
            conn.send("ack")
        except:
            conn.close()
            break

def testsendinterval(b):
    r = 0
    try:
        while True:
            r = r + 1
            time.sleep(1)
            b.send("lalalalalala" + str(r))
    except:
        pass

def listen():
    newport = get_free_port()
    write_port(newport)

    address = ('localhost', read_port())     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=str.encode(str(hashlib.sha256(v.paths.script.encode('utf-8')).hexdigest())))
    while True:
        threading.Thread(target=MessageReceived, args=(listener.accept(),)).start()
    listener.close()

v.persistentcon = False


def persistantrecv(con):
    msg = ''
    while True:
        try:
            msg = con.recv()
                        
            print("\u001B[s", end="")     # Save current cursor position
            print("\u001B[A", end="")     # Move cursor up one line
            print("\u001B[999D", end="")  # Move cursor to beginning of line
            print("\u001B[S", end="")     # Scroll up/pan window down 1 line
            print("\u001B[L", end="")     # Insert new line
            print(msg, end="")     # Print output status msg
            print("\u001B[u", end="", flush=True)     # Jump back to saved cursor position            
            #print(msg)
        except:
            break

def connect():
    try:
        address = ('localhost', read_port())
        v.persistentcon = Client(address, authkey=str.encode(str(hashlib.sha256(v.paths.script.encode('utf-8')).hexdigest())))
        threading.Thread(target=persistantrecv, args=(v.persistentcon,)).start()
    except:
        print("Mok not running? Start mok master first.")
        sys.exit()

def disconnect():
    v.persistentcon.close()

def persistentsend(data):
    v.persistentcon.send(data)

