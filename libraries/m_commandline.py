import getopt
import sys

method = False
parameters = {}

commandlineoptions = sys.argv[1:]

if len(commandlineoptions) > 0:
    method = sys.argv[1].upper()
    if len(commandlineoptions) > 1:
        parameters = commandlineoptions[1:]

def get(paramid):
    try:
        return parameters[paramid]
    except:
        return False

def getMethod():
    return method

def getValue(param, default = False):
    try:
        index = parameters.index(param)
        try:
            return parameters[index+1]
        except:
            return default
    except:
        return default
    
def isParam(param):
    try:
        index = parameters.index(param)
        return True
    except:
        return False