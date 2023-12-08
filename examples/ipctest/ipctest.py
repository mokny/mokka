import time
import os
import sys
import uuid
import mokkalib

print("Welcome to the IPC Example!")

# This has to be done in your main file
mokkalib.init()

# Getting the version as array
version = mokkalib.getVersion()
print('Version:' + str(version))

# Setting up an Eventhandler to receive Messages from Mokka or other modules
def eventHandler(msg):
    print("--->  " + str(msg))

mokkalib.setEventHandler(eventHandler)

# Triggering a global event
mokkalib.triggerGlobalEvent('Moinsen')

print("API Server:")
print(mokkalib.getApi())

# Get the workspace we are running in
print("My Workspace: " + mokkalib.getWorkspace())

# Check if another module is running: IDENT, WORKSPACE (optional)
# If you do not define a workspace, the own workspace will be used
print("Is IPCTEST running?: " + str(mokkalib.moduleIsRunning('IPCTEST')))


# Check if another module is installed params: IDENT, WORKSPACE (optional)
# If you do not define a workspace, the own workspace will be used
print("Is IPCTEST installed?: " + str(mokkalib.moduleExists('IPCTEST')))


print("Receiving Events...")

i=0
while True:
    mokkalib.triggerGlobalEvent(str(i))
    i+=1
    time.sleep(3)
