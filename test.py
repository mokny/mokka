import sys

print("I a m a atest")

def in_venv():
    return sys.prefix != sys.base_prefix


print(in_venv())