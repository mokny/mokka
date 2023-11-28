import threading
import uuid
from multiprocessing.connection import Listener, Client
import toml
import os
import pathlib
import uuid

tlock = threading.Lock()

client = False
config = False

eventHandler = False
messageHandler = False
responseHandler = False

def readConfig():
    path = 'mokka.toml'
    if os.path.isfile(path):
        try:
            f = open(path, "r")
            data = f.read()
            f.close()
            modcfg = toml.loads(data)
            return modcfg
        except:
            return False
    else:
        return False


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
                    self.msgHandler(msg)
            except Exception as err:
                break

    def send(self, data):
        self.conn.send(data)

    def disconnect(self):
        self.conn.close()

def getPort(path):
    try:
        f = open(path, "r")
        return int(f.read())
    except:
        return 6888

def getSecret(path):
    try:
        f = open(path, "r")
        return f.read()
    except:
        return False

def msgHandler(msg):
    try:
        method = msg['method']
        data = msg['data']

        if method.upper() == 'MSG':
            if messageHandler:
                messageHandler(data)

        if method.upper() == 'EVENT':
            if eventHandler:
                eventHandler(data)

        if method.upper() == 'RESPONSE':
            if responseHandler:
                responseID = msg['requestid']
                responseHandler(responseID, data)

    except:
        pass

def setEventHandler(e = False):
    global eventHandler
    eventHandler = e

def setMessageHandler(e = False):
    global messageHandler
    messageHandler = e

def setResponseHandler(e = False):
    global responseHandler
    responseHandler = e

def getWorkspace():
    return os.path.basename(os.path.dirname(pathlib.Path("../").parent.absolute()))

def getModuleName():
    return os.path.basename(os.path.dirname(pathlib.Path("./").parent.absolute()))

def request(method, data = False):
    requestid = getWorkspace() + '/' + config['GENERAL']['ident'] + '/' + str(uuid.uuid4())
    if client:
        client.send({'method': 'REQUEST', 'rmethod': method, 'requestid': requestid, 'data': data})
        return requestid


def init():
    global client
    global config
    config = readConfig()
    try:
        address = ('localhost', getPort('../../.ipcport'))
        conn = Client(address, authkey=str.encode(str(getSecret('../../.ipctoken'))))
        client = IPCOutgoingConnection(conn, msgHandler)
        client.start()
        client.send({'method': 'IMMODULE', 'data': {'ident': config['GENERAL']['ident'], 'workspace': getWorkspace()}})
    except Exception as err:
        print("MOKKA: Could not connect to parent process")
        os._exit(1)

init()