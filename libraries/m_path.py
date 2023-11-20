import os, sys
import inspect

def hasWritePermission(path):
    if os.access(path, os.W_OK):
        return True
    else:
        return False
    
def pathUser():
    return os.path.expanduser('~')

def pathAbsolute():
    return os.path.abspath(str(os.path.dirname(os.path.abspath(__file__))) + '/..')
    
def pathScript():
    return os.path.abspath(str(os.path.dirname(os.path.abspath(__file__))) + '/../' + sys.argv[0])

def changeToScriptCWD():
    os.chdir(pathAbsolute())
   
def getCWD():
    return os.getcwd()

#def setup(initfile):
#    v.paths = Paths()
#    v.paths.user = os.path.expanduser('~')
#    v.paths.script = os.path.abspath(initfile)
#    v.paths.base = os.path.dirname(v.paths.script)