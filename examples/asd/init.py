import time
import os
import sys
import uuid
import mokkalib as mokka

mokka.init()
result = mokka.request("MODINIT","fgh")
print(result)

def eventHandler(msg):
    print("--->  " + str(msg))

mokka.setEventHandler(eventHandler)
mokka.triggerGlobalEvent('Moinsen')

def in_venv():
    return sys.prefix != sys.base_prefix

print("Virtual Environment: " + str(in_venv()))

print("Here is the asd")
print(os.getcwd())
i=0
while True:
    print(str(uuid.uuid4()) + ' - Cycle: ' +  str(i))
    i+=1
    time.sleep(20)
print("Okay?")