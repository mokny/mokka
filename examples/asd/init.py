import time
import os
import sys
import uuid
import mokkalib

# This has to be done in your main file
mokkalib.init()

# Sending a raw request
result = mokkalib.request("MODINIT","fgh")
print(result)

# Getting the version as array
version = mokkalib.getVersion()
print('Version:' + str(version))

# Setting up an Eventhandler to receive Messages from Mokka or other modules
def eventHandler(msg):
    print("--->  " + str(msg))

mokkalib.setEventHandler(eventHandler)

# Triggering a global event
mokkalib.triggerGlobalEvent('Moinsen')

print(mokkalib.getApi())

# Get the workspace we are running in
print("My Workspace: " + mokkalib.getWorkspace())

# Check if another module is running: IDENT, WORKSPACE (optional)
# If you do not define a workspace, the own workspace will be used
print("Is BLA running?: " + str(mokkalib.moduleIsRunning('BLA')))


# Check if another module is installed params: IDENT, WORKSPACE (optional)
# If you do not define a workspace, the own workspace will be used
print("Is BLA installed?: " + str(mokkalib.moduleExists('BLA')))

if not mokkalib.moduleExists('BLA'):
    print("Installing bla..")
    # Install another module
    mokkalib.install('examples/bla')
    print("Is it now installed?: " + str(mokkalib.moduleExists('BLA')))

print("Trying to run bla")
# Run another module. Param2 can be a workspace. if not defined, own workspace will be used
print(mokkalib.runModule('BLA'))


print("Removing BLA")
# Removing another module. Param2 can be a workspace. if not defined, own workspace will be used
print(mokkalib.remove('BLA'))

print("Here is the asd")
print(os.getcwd())

i=0
while True:
    mokkalib.triggerGlobalEvent(str(i))
    print(str(uuid.uuid4()) + ' - Cycle: ' +  str(i))
    i+=1
    time.sleep(5)
print("Okay?")