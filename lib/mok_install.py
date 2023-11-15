import subprocess
import sys

def pip_package_install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install():
    pip_package_install('GitPython')
    pip_package_install('virtualenv')