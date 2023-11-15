import os, shutil
import mok_vars as v

class Paths:
    user =  ''
    script = ''
    base = ''


def setup(initfile):
    v.paths = Paths()
    v.paths.user = os.path.expanduser('~')
    v.paths.script = os.path.abspath(initfile)
    v.paths.base = os.path.dirname(v.paths.script)

