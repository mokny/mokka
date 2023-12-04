#!/usr/bin/python3
import threading
import time
import uuid
import random
from multiprocessing.connection import Listener, Client
from contextlib import closing
import socket
import os
import sys
import tomllib 

tlock = threading.Lock()
client = False
secret = False
port = False
initialized = False
config = {}
eventHandler = False

class IPCOutgoingConnection(threading.Thread):
    def __init__(self, conn):  
        threading.Thread.__init__(self)
        self.conn = conn
        self.eventHandler = False

    def run(self):
        self.initConnection()
        msg = ''
        while True:
            try:
                msg = self.conn.recv()
                with tlock:
                    if self.eventHandler:
                        self.eventHandler(msg)
            except Exception as err:
                break

    def initConnection(self):
        self.send({'type': 'REQUEST', 'mod': config['GENERAL']['ident'].upper(), 'method': 'MODPIPE', 'payload': 'MY'})

    def send(self, data):
        self.conn.send(data)

    def disconnect(self):
        self.conn.close()

    def setEventHandler(self, evh):
        self.eventHandler = evh

def pathBase():
    pb = os.path.join(os.path.expanduser('~'), 'mokkabase')
    if not os.path.isdir(pb):
        os.mkdir(pb)
    return pb

def request(method, payload):
    global secret, port, config, initialized
    address = ('127.0.0.1', port)
    con = Client(address, authkey=str.encode(str(secret)))
    if con:
        con.send({'type': 'REQUEST', 'mod': config['GENERAL']['ident'].upper(), 'method': method, 'payload': payload})
        msg = con.recv()
        con.close()
        return msg
    return False

def setEventHandler(evh):
    global client
    client.setEventHandler(evh)

def init():
    global secret, port, config, initialized, client
    if not initialized:
        secret = ''
        with open(os.path.join(pathBase(),'.secret'), "r") as f:
            secret = str(f.read())
        
        port = 6888
        with open(os.path.join(pathBase(),'.port'), "r") as f:
            port = int(f.read())
    
        config = {}
        with open("mokka.toml", "r") as f:
            tomlraw = f.read()
        config = tomllib.loads(tomlraw)

        # Constant PIPE for receiving events
        address = ('127.0.0.1', port)
        conn = Client(address, authkey=str.encode(str(secret)))
        client = IPCOutgoingConnection(conn)
        client.start()

        initialized = True
