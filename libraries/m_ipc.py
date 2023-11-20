import threading
import time
import uuid
import random
from multiprocessing.connection import Listener, Client
from contextlib import closing
import socket

tlock = threading.Lock()

class IPCServer(threading.Thread):
    def __init__(self, msgHandler, port, secret):  
        threading.Thread.__init__(self)
        self.msgHandler = msgHandler
        self.port = port
        self.secret = secret

    def run(self):
        address = ('localhost', self.port)     # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=str.encode(str(self.secret)))
        while True:
            c = IPCIncomingConnection(listener.accept(), self.msgHandler)
            c.start()


class IPCIncomingConnection(threading.Thread):
    def __init__(self, conn, msgHandler):  
        threading.Thread.__init__(self)
        self.conn = conn
        self.msgHandler = msgHandler

    def run(self):
        msg = ''
        while True:
            try:
                msg = self.conn.recv()
                with tlock:
                    self.msgHandler(self, msg)
            except Exception as err:
                self.conn.close()
                break

    def send(self, data):
        self.conn.send(data)

    def disconnect(self):
        self.conn.close()

class IPCOutgoingConnection(threading.Thread):
    def __init__(self, conn, msgHandler):  
        threading.Thread.__init__(self)
        self.conn = conn
        self.msgHandler = msgHandler

    def run(self):
        msg = ''
        while True:
            try:
                msg = self.conn.recv()
                with tlock:
                    self.msgHandler(self, msg)
            except Exception as err:
                break

    def send(self, data):
        self.conn.send(data)

    def disconnect(self):
        self.conn.close()


def createPort(path):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            f = open(path, "w")
            f.write(str(s.getsockname()[1]))
            f.close()
        except:
            return 6888

def getPort(path):
    try:
        f = open(path, "r")
        return int(f.read())
    except:
        return 6888

def createSecret(path):
    try:
        newsecret = str(uuid.uuid4()) + str(random.randint(10000,99999)) + str(time.time())
        f = open(path, "w")
        f.write(newsecret)
        f.close()
    except:
        return False

def getSecret(path):
    try:
        f = open(path, "r")
        return f.read()
    except:
        return False

def startServer(msgHandler, portpath, secretpath):
    return IPCServer(msgHandler, getPort(portpath), getSecret(secretpath)).start()

def startClient(msgHandler, portpath, secretpath):
    try:
        address = ('localhost', getPort(portpath))
        conn = Client(address, authkey=str.encode(str(getSecret(secretpath))))
        client = IPCOutgoingConnection(conn, msgHandler)
        client.start()
        return client
    except:
        return False



