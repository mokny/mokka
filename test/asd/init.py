import time
import os
import sys

def in_venv():
    return sys.prefix != sys.base_prefix

print("Virtual Environment: " + str(in_venv()))

print("Here is the asd")
print(os.getcwd())
i=0
while True:
    print("hay " + str(i))
    i+=11
    time.sleep(1)
print("Okay?")