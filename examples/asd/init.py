import time
import os
import sys
import uuid
import mokkalib

mokkalib.init()
result = mokkalib.request("MODINIT","fgh")
print(result)

version = mokkalib.getVersion()
print('Version:' + str(version))

def eventHandler(msg):
    print("--->  " + str(msg))

mokkalib.setEventHandler(eventHandler)
mokkalib.triggerGlobalEvent('Moinsen')

def in_venv():
    return sys.prefix != sys.base_prefix

print("Virtual Environment: " + str(in_venv()))

print("Here is the asd")
print(os.getcwd())
i=0
while True:
    mokkalib.triggerGlobalEvent(str(i))
    print(str(uuid.uuid4()) + ' - Cycle: ' +  str(i))
    i+=1
    time.sleep(5)
print("Okay?")