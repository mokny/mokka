import threading
import subprocess 
import m_handlers as handlers

class Module(threading.Thread):
    def __init__(self, con, path, executable):  
        threading.Thread.__init__(self)
        self.path = path
        self.executable = executable
        self.con = con
        

    def run(self):
        value = 'ping -c 200 google.com'
        try:
            process = subprocess.Popen(value.split(' '), stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                handlers.protreq(self.con, 'output', str(line.rstrip()))

                err = process.stderr.read()                
                if err:
                    handlers.protreq(self.con, 'output', str(err))
                    break

            handlers.protreq(self.con, 'output', "End")
        except:
            handlers.protreq(self.con, 'output', "EndErr")
            pass

        
    