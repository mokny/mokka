import time
import os
import sys
import mokka

def in_venv():
    return sys.prefix != sys.base_prefix

def eventHandler(msg):
    print("EVENT " + str(msg))
    print("Making a request...")
    rid = mokka.request('STATUS','')
    print("RequestID: " + rid)

def responseHandler(requestid, data):
    print("Got a response to " + requestid + ': ' + str(data))

mokka.setEventHandler(eventHandler)
mokka.setResponseHandler(responseHandler)

print("Virtual Environment: " + str(in_venv()))

print("Here is the asd")
print(os.getcwd())
i=0
while True:
    print("hay " + str(i))
    i+=11
    time.sleep(1)
print("Okay?")