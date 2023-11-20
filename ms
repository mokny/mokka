#!/usr/bin/python3

import os, sys, getopt
import time
import subprocess
import shutil
import signal
import logging
import threading

# Change to program path as working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Insert own lib path
sys.path.insert(0, './libraries')

# Custom libraries
import m_vars as v
import m_commandline as opt
import m_path as pt
import m_pid as pid
import m_ipc as ipc
import m_handlers as handlers


#Global Vars
v.client = False
v.server = False

#Main
def main():

    if not pt.hasWritePermission(pt.pathAbsolute()):
        print("Application directory is not writable. Exiting.")
        os._exit(1)

    print(opt.getMethod())
    print(opt.getValue('asd'))
    print(opt.isParam('quak'))

    # Kill old instances
    if opt.getMethod() == "EXIT":
        pid.kill()
        pid.removefile()
        os._exit(0)

    # Start the service after killing old instances
    if opt.getMethod() == "RUNSERVICE":
        pid.kill()
        pid.write()
        # Create connect files
        ipc.createSecret(pt.pathAbsolute() + '/.ipctoken')
        ipc.createPort(pt.pathAbsolute() + '/.ipcport')
        # Start server
        v.server = ipc.startServer(handlers.serverHandler, ipc.getPort(pt.pathAbsolute() + '/.ipcport'), ipc.getSecret(pt.pathAbsolute() + '/.ipctoken'))

    #Other Methods given
    else:

        #Start the client and try to connect to service
        v.client = ipc.startClient(handlers.clientHandler, ipc.getPort(pt.pathAbsolute() + '/.ipcport'), ipc.getSecret(pt.pathAbsolute() + '/.ipctoken'))
        if not pid.check() and not v.client: #Service not available, so restart it with nohup
            os.system("nohup "+sys.executable+" "+pt.pathScript() + " RUNSERVICE > /dev/null &")

            # Now try to connect
            retries = 0
            while retries < 10:
                time.sleep(0.2)
                v.client = ipc.startClient(handlers.clientHandler, ipc.getPort(pt.pathAbsolute() + '/.ipcport'), ipc.getSecret(pt.pathAbsolute() + '/.ipctoken'))
                if v.client: 
                    break
                retries += 1
        
        # Connection error?
        if not v.client:
            print("ERROR: Service not reachable")
            os._exit(1)

        # Main proc
    
    # If process is Server
    if v.server:
        pass

    # If process is Client
    elif v.client:
        
        while True:
            v.client.send("kakaka")
            time.sleep(1)



if __name__ == "__main__":        
    main()
