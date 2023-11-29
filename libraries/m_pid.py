import os
import signal

def write():
   f = open("workspaces/.pid", "w")
   f.write(str(os.getpid()))
   f.close()

def kill():
   try:
      f = open("workspaces/.pid", "r")
      os.kill(int(f.read()), signal.SIGKILL)
      removefile()
      return True
   except:
      return False

def check():        
   try:
      f = open("workspaces/.pid", "r")
      os.kill(int(f.read()), 0)
      return True
   except OSError:
      return False

def removefile():
   try:
      os.remove('workspaces/.pid')
   except:
      pass
