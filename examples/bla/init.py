import sys

def in_venv():
    return sys.prefix != sys.base_prefix

print("Virtual Environment: " + str(in_venv()))

print("Here is the bla")
print("Use IN BLA TEXT to enter text")
v = input()
print("You entered: " + v)
