import os
import venv
import mok_vars as v
import shutil
import subprocess
import uuid

vebasepath = os.path.join(v.wd, "ve")

if not os.path.isdir(vebasepath):
    os.mkdir(vebasepath)

def create(filename):
    ident = str(uuid.uuid4())
    if os.path.isdir(vebasepath):
        vepath = os.path.join(vebasepath, ident)
        os.mkdir(vepath)
        venv.create(vepath)
        shutil.copy(filename, vepath + '/'+filename)
        try:
            p = subprocess.Popen([vepath+"/bin/python", vepath+"/"+filename])
            p.communicate()
        except Exception as error:
            print("Error", error)
        shutil.rmtree(vepath)

def clean():
    if os.path.isdir(vebasepath):
        shutil.rmtree(vebasepath)