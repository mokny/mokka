import threading
import subprocess 
import os, signal
import m_handlers as handlers
import m_vars as v

tlock = threading.Lock()


class Module(threading.Thread):
    def __init__(self, modident, con, path, executable):  
        threading.Thread.__init__(self)
        self.modident = modident
        self.path = path
        self.executable = executable
        self.con = con
        self.process = None
        self.output = []
        self.joinedconnections = []

        with tlock:
            v.modules[self.modident] = self

        self.join(self.con)

    def join(self, con):
        if not con in self.joinedconnections:
            self.joinedconnections.append(con)

    def part(self, con):
        try:
            self.joinedconnections.remove(con)
        except:
            pass

    def out(self, msg):
        with tlock:
            for con in self.joinedconnections:
                try:
                    handlers.protreq(con, 'output', str('['+self.modident+'] ') +  str(msg))
                except:
                    self.part(con)

    def sendInput(self, text):
        print(text, file=self.process.stdin, flush=True)

    def kill(self):
        self.process.kill()

    def run(self):
        value = 'ping -c 10000 localhost'
        #value = '/usr/bin/python3 test.py'
        try:
            self.process = subprocess.Popen(value.split(' '), stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid)
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.output.append(line)
                if len(self.output) > 10:
                    self.output = self.output[1:]
                self.out(str(line.rstrip()))

            err = self.process.stderr.read()          
            if err:
                self.out(str(err))

            self.output(str('END'))
        except Exception as err:
            pass

        with tlock:
            del v.modules[self.modident]
            pass


def join(con, ident):
    if ident in v.modules:
        v.modules[ident].join(con)

def partall(con):
    for module in v.modules:
        v.modules[module].part(con)

def runModule(con, ident):
    if ident in v.modules:
        handlers.protreq(con, 'output', "This module is already running")
        return
    Module(ident, con, 'asd','asd').start()