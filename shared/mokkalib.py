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

VERSION = ['0','1','1']

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
                        if 'payload' in msg:
                            self.eventHandler(msg['payload'])

            except Exception as err:
                break

    def initConnection(self):
        self.send({'type': 'PIPE', 'pid': 'p'+str(os.getpid()), 'method': 'MODPIPE', 'payload': 'MY'})

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

def getVersion():
    res = request('VERSION', False)
    return {'DAEMON': res['payload'], 'LIB': VERSION}

def getWorkspace():
    res = request('GETWORKSPACE', True)
    return res['payload']


def runModule(module, workspace = False):
    res = request('RUN', {'workspace': workspace, 'module': module})
    return res['payload']

def moduleExists(module, workspace = False):
    res = request('MODULEEXISTS', {'workspace': workspace, 'module': module})
    return res['payload']

def moduleIsRunning(module, workspace = False):
    res = request('MODULEISRUNNING', {'workspace': workspace, 'module': module})
    return res['payload']

def install(module, workspace = False):
    res = request('INSTALL', {'workspace': workspace, 'module': module})
    return res['payload']

def remove(module, workspace = False):
    res = request('REMOVE', {'workspace': workspace, 'module': module})
    return res['payload']

def kill(module, workspace = False):
    res = request('KILL', {'workspace': workspace, 'module': module})
    return res['payload']

def getLog(module, workspace = False):
    res = request('GETLOG', {'workspace': workspace, 'module': module})
    return res['payload']

def getApi():
    res = request('GETAPI', True)
    return res['payload']

def getOption(option, default = None, module = False, workspace = False):
    res = request('GETOPTION', {'workspace': workspace, 'module': module, 'option': option, 'default': default})
    return res['payload']

def setOption(option, value, module = False, workspace = False):
    res = request('SETOPTION', {'workspace': workspace, 'module': module, 'option': option, 'value': value})
    return res['payload']

def workspaceCreate(workspace):
    res = request('WORKSPACECREATE', workspace)
    return res['payload']

def workspaceRemove(workspace):
    res = request('WORKSPACEREMOVE', workspace)
    return res['payload']

def request(method, payload):
    global secret, port, config, initialized
    address = ('127.0.0.1', port)
    con = Client(address, authkey=str.encode(str(secret)))
    if con:
        con.send({'type': 'REQUEST', 'pid': 'p'+str(os.getpid()), 'method': method, 'payload': payload})
        msg = con.recv()
        con.close()
        return msg
    return False

def triggerGlobalEvent(message):
    request('GLOBALEVENT', message)

def setEventHandler(evh):
    global client
    client.setEventHandler(evh)

def exit():
    sys.exit()
    os.exit()

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
