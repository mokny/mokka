import sys

print("Testfile")
v = input("Please enter your name: ")
print("Result " + v)
def in_venv():
    return sys.prefix != sys.base_prefix


print(in_venv())