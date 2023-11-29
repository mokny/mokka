import threading
import subprocess 
import os, signal
import m_handlers as handlers
import m_vars as v
import toml
import shutil
import venv
import sys
import psutil

tlock = threading.Lock()


class Module(threading.Thread):
    def __init__(self, modident, con, path, executable):  
        threading.Thread.__init__(self)
        self.modident = modident
        self.path = path
        self.executable = executable
        self.con = con
        self.process = None
        self.output = []
        self.joinedconnections = []
        self.workspace = con.workspace
        self.ipcconnection = False
        self.ps = False

        self.config = {}

        with tlock:
            if not self.workspace in v.modules:
                v.modules[self.workspace] = {}
            v.modules[self.workspace][self.modident] = self

        self.join(self.con)

    def readConfig(self):
        path = '../workspaces/' + self.workspace + '/' + self.modident + '/mokka.toml'
        if os.path.isfile(path):
            try:
                f = open(path, "r")
                data = f.read()
                f.close()
                modcfg = toml.loads(data)
                return modcfg
            except:
                return False
        else:
            return False


    def join(self, con):
        if not con in self.joinedconnections:
            self.joinedconnections.append(con)

    def part(self, con):
        try:
            self.joinedconnections.remove(con)
        except:
            pass

    def out(self, msg):
        with tlock:
            for con in self.joinedconnections:
                try:
                    handlers.protreq(con, 'output', str('['+self.workspace+'/') + str(self.modident+'] ') +  str(msg))
                except:
                    self.part(con)

    def sendInput(self, text):
        print(text, file=self.process.stdin, flush=True)

    def kill(self):
        self.process.kill()

    def run(self):
        self.config = self.readConfig()
        if self.config:
            
            value = 'ping -c 10000 localhost' 
            #value = '/usr/bin/python3 test.py'

            command = ''
            command = self.config['GENERAL']['python'] + ' '
            command += self.config['GENERAL']['exec'] + ' '

            self.out('Running ' + self.config['GENERAL']['title'])
            value = command
            try:
                os.environ["PYTHONUNBUFFERED"] = "1"
                self.process = subprocess.Popen(value.split(' '), stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, preexec_fn=os.setsid, cwd='workspaces/' + self.workspace + '/' + self.modident)
                self.ps = psutil.Process(self.process.pid)

                while True:
                    line = self.process.stdout.readline()
                    self.process.stdout.flush()
                    if not line:
                        break
                    self.output.append(line)
                    if len(self.output) > 10:
                        self.output = self.output[1:]
                    self.out(str(line.rstrip()))

                err = self.process.stderr.read()          
                if err:
                    self.out(str(err))

                self.out(str('-- END --'))
            except Exception as err:
                self.out(str('-- END WITH ERR ' + str(err) + ' --'))
                pass
        else:
            self.out(str('Config failure'))

        with tlock:
            del v.modules[self.workspace][self.modident]
            pass

    def getPerformance(self):
        ret = {
                    'cpu_time': self.ps.cpu_times().system,
                    'cpu_percent': self.ps.cpu_percent() / psutil.cpu_count(),
                    'status': self.ps.status(),
        }
        return ret
    
def join(con, ident):
    if ident in v.modules[con.workspace]:
        v.modules[con.workspace][ident].join(con)

def partall(con):
    for module in v.modules[con.workspace]:
        v.modules[con.workspace][module].part(con)

def runModule(con, ident):
    if ident in v.modules[con.workspace]:
        handlers.protreq(con, 'output', "This module is already running")
        return
    handlers.protreq(con, 'output', 'Running ' + ident + ' in ws ' + con.workspace)
    Module(ident, con, 'asd','asd').start()

    
def check(con, path):
    if os.path.isfile(path + '/mokka.toml'):
        try:
            f = open(path + '/mokka.toml', "r")
            data = f.read()
            f.close()
            modcfg = toml.loads(data)
            if not modcfg['GENERAL']['ident']: 
                handlers.protreq(con, 'output', "'ident' is missing in mokka.toml")
                return False
            if not modcfg['GENERAL']['title']: 
                handlers.protreq(con, 'output', "'title' is missing in mokka.toml")
                return False
            if not modcfg['GENERAL']['exec']: 
                handlers.protreq(con, 'output', "'exec' is missing in mokka.toml")
                return False
            if not os.path.isfile(path + '/' + modcfg['GENERAL']['exec']):
                handlers.protreq(con, 'output', "Executable file " +  modcfg['GENERAL']['exec'] + " is missing")
                return False
            if os.path.isdir('workspaces/' + con.workspace + '/' + modcfg['GENERAL']['ident']):
                handlers.protreq(con, 'output', "Module " +  modcfg['GENERAL']['ident'] + " already exists")
                return False

            return modcfg
        except:
            handlers.protreq(con, 'output', "Invalid toml")
            return False
    else:
        handlers.protreq(con, 'output', "No toml")
        return False

def kill(workspace, ident):
    if workspace in v.modules:
        if ident in v.modules[workspace]:
            v.modules[workspace][ident].kill()

def installFromPath(con, origin):
    modcfg = check(con, origin)
    if modcfg:
        try:
            modpath = 'workspaces/' + con.workspace + '/' + modcfg['GENERAL']['ident']
            if modcfg['GENERAL']['venv']:
                handlers.protreq(con, 'output', "Creating virtual environment...")
                os.mkdir(modpath)
                venv.create(modpath)
                if 'piplibs' in modcfg['INSTALL']:
                    handlers.protreq(con, 'output', "Installing PIP...")
                    subprocess.check_call([modpath + '/' + modcfg['GENERAL']['python'], '-m' , 'ensurepip', '--default-pip'])
                    handlers.protreq(con, 'output', "Installing TOML...")
                    subprocess.check_call([modpath + '/' + modcfg['GENERAL']['python'], "-m", "pip", "install", 'toml'])
                    for piplib in modcfg['INSTALL']['piplibs']:
                        handlers.protreq(con, 'output', "Installing " + piplib + '...')
                        subprocess.check_call([modpath + '/' + modcfg['GENERAL']['python'], "-m", "pip", "install", piplib])
            handlers.protreq(con, 'output', 'Copying files...')
            shutil.copytree(origin, modpath, dirs_exist_ok=True)
            handlers.protreq(con, 'output', 'Copying ipc modules...')
            shutil.copy('shared/mokka.py', modpath + '/mokka.py')
            handlers.protreq(con, 'output', "Installation complete!")
            return True
        except Exception as err:
            handlers.protreq(con, 'output', str(err))
            handlers.protreq(con, 'output', "Installation failed.")
        return True
    
    return 'Installation failed.'

def getModulesByWorkspace(workspace):
    ret = {}
    for ident in os.listdir("workspaces/" + workspace):
        if os.path.isdir("workspaces/"+workspace + '/' + ident):
            module = {
                'ident': ident,
                'path': "workspaces/"+workspace,
            }
            ret[ident] = module
    return ret

def getModulesRunningByWorkspace(workspace):
    ret = {}
    if not workspace in v.modules:
        v.modules[workspace] = {}

    for module in v.modules[workspace]:
        ret[module] = v.modules[workspace][module]
    return ret
        
