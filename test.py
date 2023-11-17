import sys

print("I a m a atest")
v = input()
print(v)

def in_venv():
    return sys.prefix != sys.base_prefix


print(in_venv())