import m_ipc
import os
import shutil
from subprocess import Popen, PIPE

import m_module as m
import m_vars as v

def protreq(con, method, data):
    payload = {
        'method': method,
        'data': data
    }
    con.send(payload)

def protdisc(con):
    protreq(con, 'disconnect')

def protinput(con):
    protreq(con, 'input')

def serverHandler(con, data = False):
    try:
        # In App console commands
        if data['method'].upper() == 'INPUT':
            commands(con, data['data'])

        # Shell passthru
        elif data['method'].upper() == 'COMMANDLINE':
            if data['data'][0].upper() == 'STATUS':
                protreq(con, 'output', 'Service is up and running')
                protdisc(con)

            elif data['data'][0].upper() == 'HELP':
                protreq(con, 'output', 'GENERAL COMMANDS')
                protreq(con, 'output', ' HELP')
                protreq(con, 'output', ' SHUTDOWN')
                protreq(con, 'output', ' STATUS')
                protreq(con, 'output', ' CONSOLE')
                protdisc(con)
            
            elif data['data'][0].upper() == 'CONSOLE':
                protreq(con, 'clear', con.workspace)
                protreq(con, 'inputenabled', con.workspace)

                protreq(con, 'output', '              _    _          ')
                protreq(con, 'output', '  /\/\   ___ | | _| | ____ _  ')
                protreq(con, 'output', ' /    \ / _ \| |/ / |/ / _` | ')
                protreq(con, 'output', '/ /\/\ \ (_) |   <|   < (_| |') 
                protreq(con, 'output', '\/    \/\___/|_|\_\_|\_\__,_|')
                protreq(con, 'output', '')
                protreq(con, 'output', '* * * * * * * * * * * * * * * * * * *')
                protreq(con, 'output', '*  by T.Vennefrohne 4 TxAV          *')
                protreq(con, 'output', '*  Shell. Type EXIT or Q to quit    *')
                protreq(con, 'output', '* * * * * * * * * * * * * * * * * * *')
                protreq(con, 'output', '')


            else:
                protreq(con, 'output', 'Use HELP for more information. Exiting.')
                protdisc(con)

    except:
        protdisc(con)




def out(msg):
    print("\u001B[s", end="")     # Save current cursor position
    print("\u001B[A", end="")     # Move cursor up one line
    print("\u001B[999D", end="")  # Move cursor to beginning of line
    print("\u001B[S", end="")     # Scroll up/pan window down 1 line
    print("\u001B[L", end="")     # Insert new line
    print(msg, end="")     # Print output status msg
    print("\u001B[u", end="", flush=True)     # Jump back to saved cursor position            
     
def commands(con, cmd):

    try:
        parts = cmd.split(" ")
        
        if len(parts) > 0:
            method = parts[0].upper()


            if method == 'EXIT' or method == 'Q':
                m.partall(con)
                protdisc(con)
            elif method == 'HELP':
                protreq(con, 'inputenabled', con.workspace)
                protreq(con, 'output', 'Commands:')
                protreq(con, 'output', ' HELP               - This help document')
                protreq(con, 'output', ' EXIT or Q          - Exit the shell')
                protreq(con, 'output', ' SHUTDOWN           - Shutdown the service')
                protreq(con, 'output', ' ABOUT              - About this software')
                protreq(con, 'output', ' RUN <IDENT>        - Run subprocess')
                protreq(con, 'output', ' PART <IDENT>       - Part subprocess output')
                protreq(con, 'output', ' PARTALL            - Part all subprocess outputs')
                protreq(con, 'output', ' LIST               - List all running subprocesses')
                protreq(con, 'output', ' GETLOG <IDENT>     - Get log of subprocess')
                protreq(con, 'output', ' MARKET             - Marketplace')
                protreq(con, 'output', ' MODULE or MOD      - Modules')
                protreq(con, 'output', ' IN <IDENT> <DATA>  - Send input to process')
                protreq(con, 'output', ' KILL <IDENT>       - Kill subprocess')
                protreq(con, 'output', ' INFO <IDENT>       - Details about a subprocess')
                protreq(con, 'output', ' KILLALL            - Kill all subprocesses')
                protreq(con, 'output', ' WS                 - Workspace')
            elif method == 'ABOUT':
                protreq(con, 'inputenabled', con.workspace)
                protreq(con, 'output', 'Mokka - by Till Vennefrohne 2023')
            elif method == 'SHUTDOWN':
                os._exit(0)
            elif method == 'RUN':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                protreq(con, 'output', 'Ident: ' + ident)
                m.runModule(con, ident)
            elif method == 'PARTALL':
                protreq(con, 'inputenabled', con.workspace)
                protreq(con, 'output', 'Parting all modules')
                m.partall(con)
                pass
            elif method == 'IN':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                if ident in v.modules:
                    oparts = parts[2:]
                    inp = ' '.join(oparts)
                    v.modules[ident].sendInput(inp)
                else:
                    protreq(con, 'output', 'Module ' + ident + ' is not running')
            elif method == 'JOIN':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                if ident in v.modules:
                    protreq(con, 'output', 'Joining ' + ident)
                    m.join(con, ident)
                else:
                    protreq(con, 'output', 'Module ' + ident + ' is not running')
            elif method == 'PART':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                if ident in v.modules:
                    v.modules[ident].part(con)
                    protreq(con, 'output', 'Parting ' + ident)
                else:
                    protreq(con, 'output', 'Module ' + ident + ' is not running')
            elif method == 'KILL':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                if ident in v.modules:
                    v.modules[ident].kill()
                else:
                    protreq(con, 'output', 'Module ' + ident + ' is not running')
            elif method == 'INFO':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                if ident in v.modules:
                    protreq(con, 'output', 'Joined clients ' + str(len(v.modules[ident].joinedconnections)))
                else:
                    protreq(con, 'output', 'Module ' + ident + ' is not running')
            elif method == 'KILLALL':
                protreq(con, 'inputenabled', con.workspace)
                protreq(con, 'output', 'Killed all running modules')
                for ident in v.modules:
                    v.modules[ident].kill()
            elif method == 'LIST':
                protreq(con, 'inputenabled', con.workspace)
                protreq(con, 'output', 'Running modules:')
                protreq(con, 'output', '- - - - - - - - - - - - -')
                for ident in v.modules:
                    protreq(con, 'output', '[' + ident + ']')
                protreq(con, 'output', '- - - - - - - - - - - - -')
            elif method == 'GETLOG':
                protreq(con, 'inputenabled', con.workspace)
                ident = parts[1].upper()
                if ident in v.modules:
                    log = v.modules[ident].output
                    for line in log:
                        protreq(con, 'output', line)
            elif method == 'MARKET':
                protreq(con, 'inputenabled', con.workspace)
                if len(parts) >= 2:
                    if parts[1].upper() == 'HELP':
                        protreq(con, 'output', 'MARKET SEARCH <TERM>')
                        protreq(con, 'output', 'MARKET INSTALL <IDENT>')
                        protreq(con, 'output', 'MARKET HELP')
                    elif parts[1].upper() == 'SEARCH':
                        oparts = parts[2:]
                        term = ' '.join(oparts)
                        protreq(con, 'output', term + ' not found')
                    elif parts[1].upper() == 'INSTALL':
                        oparts = parts[2:]
                        term = ' '.join(oparts)
                        protreq(con, 'output', term + ' not found')
                    else:
                        protreq(con, 'output', 'Use MARKET HELP')
                else:
                    protreq(con, 'output', 'Use MARKET HELP')
                    pass
            elif method == 'MODULE' or method == 'MOD':
                protreq(con, 'inputenabled', con.workspace)
                if len(parts) >= 2:
                    if parts[1].upper() == 'HELP':
                        protreq(con, 'output', 'MODULE CREATE <IDENT> <PATH>')
                        protreq(con, 'output', 'MODULE INSTALL <IDENT> <PATH>')
                        protreq(con, 'output', 'MODULE HELP')
                        protreq(con, 'output', 'MODULE REMOVE <IDENT>')
                        protreq(con, 'output', 'MODULE RUN <IDENT>')
                    elif parts[1].upper() == 'CREATE':
                        oparts = parts[3:]
                        path = ' '.join(oparts)
                        try:
                            shutil.copytree(path, 'workspaces/' + con.workspace + '/' + parts[2])
                            protreq(con, 'output', 'Installed.')
                        except Exception as err:
                            protreq(con, 'output', str(err))

                    elif parts[1].upper() == 'REMOVE':
                        oparts = parts[2:]
                        ident = ' '.join(oparts)
                        shutil.rmtree('workspaces/'+ con.workspace + '/' + ident)
                    elif parts[1].upper() == 'RUN':
                        oparts = parts[2:]
                        ident = ' '.join(oparts)
                        m.runModule(con, ident.upper())
                    elif parts[1].upper() == 'INSTALL':
                        oparts = parts[3:]
                        path = ' '.join(oparts)
                        try:
                            shutil.copytree(path, 'workspaces/' + con.workspace + '/' + parts[2])
                            protreq(con, 'output', 'Installed.')
                        except Exception as err:
                            protreq(con, 'output', str(err))
                    else:
                        protreq(con, 'output', 'Use MODULE HELP')
                else:
                    protreq(con, 'output', 'Use MODULE HELP')
                    pass
            elif method == 'WORKSPACE' or method == 'WS':
                if len(parts) >= 2:
                    if parts[1].upper() == 'HELP':
                        protreq(con, 'inputenabled', con.workspace)
                        protreq(con, 'output', 'WORKSPACE CREATE <IDENT>')
                        protreq(con, 'output', 'WORKSPACE REMOVE <IDENT>')
                        protreq(con, 'output', 'WORKSPACE SET <IDENT>')
                        protreq(con, 'output', 'WORKSPACE LIST')
                        protreq(con, 'output', 'WORKSPACE REMOVE <IDENT>')
                    elif parts[1].upper() == 'CREATE':
                        ident = parts[2].upper()
                        try:
                            os.mkdir('workspaces/' + ident)
                            con.workspace = ident
                            protreq(con, 'inputenabled', con.workspace)
                            protreq(con, 'workspace', v.workspace)
                            protreq(con, 'output', 'Workspace created.')
                        except Exception as err:
                            protreq(con, 'inputenabled', con.workspace)
                            protreq(con, 'output', 'Failed. Maybe workspace already exists?')
                    elif parts[1].upper() == 'SET':
                        ident = parts[2].upper()
                        if os.path.isdir('workspaces/' + ident):
                            con.workspace = ident
                            protreq(con, 'inputenabled', con.workspace)
                            protreq(con, 'output', 'Workspace switched')
                        else:
                            protreq(con, 'inputenabled', con.workspace)
                            protreq(con, 'output', 'Workspace does not exist.')
                    elif parts[1].upper() == 'LIST':
                        protreq(con, 'inputenabled', con.workspace)
                        for name in os.listdir("workspaces/."):
                            if os.path.isdir("workspaces/"+name):
                                protreq(con, 'output', '- ' + name)
                    elif parts[1].upper() == 'REMOVE' or  parts[1].upper() == 'RM':
                        try:
                            ident = parts[2].upper()
                            if ident != "":
                                if ident == con.workspace:
                                    con.workspace = 'DEFAULT'
                                    
                                if ident == 'DEFAULT':
                                    protreq(con, 'inputenabled', con.workspace)
                                    protreq(con, 'output', 'The DEFAULT workspace can not be removed.')
                                else:
                                    if os.path.isdir("workspaces/"+ident):
                                        try:
                                            shutil.rmtree("workspaces/"+ident)
                                            protreq(con, 'inputenabled', con.workspace)
                                            protreq(con, 'output', 'Workspace removed.')
                                        except:
                                            protreq(con, 'inputenabled', con.workspace)
                                            protreq(con, 'output', 'Workspace could not be removed.')
                                    else:
                                        protreq(con, 'inputenabled', con.workspace)
                                        protreq(con, 'output', 'Workspace could not be removed.')
                            else:
                                protreq(con, 'inputenabled', con.workspace)
                                protreq(con, 'output', 'Workspace could not be removed.')
                        except:
                            protreq(con, 'inputenabled', con.workspace)
                            protreq(con, 'output', 'Workspace could not be removed.')
                else:
                    protreq(con, 'inputenabled', con.workspace)
                    protreq(con, 'output', 'Unknown command. Type WORKSPACE HELP')
            else:
                protreq(con, 'inputenabled', con.workspace)
                protreq(con, 'output', 'Unknown command. Type HELP')
        else:
            protreq(con, 'inputenabled', con.workspace)
            protreq(con, 'output', 'Unknown command. Type HELP')
    except Exception as err:
        protreq(con, 'inputenabled', con.workspace)
        protreq(con, 'output', str(err))

def clientHandler(con, data):
       
        if data['method'] == 'output':
            out(data['data'])

        if data['method'] == 'clear':
            os.system('clear')
            for i in range(200):
                print('')

        if data['method'] == 'input':
            protreq(con,'input',input())

        if data['method'] == 'disconnect':
            os._exit(0)

        if data['method'] == 'workspace':
            v.workspace = data['data']

        if data['method'] == 'inputenabled':
            print('MOKKA [' + data['data'] + ']> ',end="") 

