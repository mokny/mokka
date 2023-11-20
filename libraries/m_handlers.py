import m_ipc
import os

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
            if data['data'].upper() == 'EXIT':
                protdisc(con)
            elif data['data'].upper() == 'HELP':
                protreq(con, 'output', 'Commands:')
                protreq(con, 'output', ' HELP       - This help document')
                protreq(con, 'output', ' EXIT       - Exit the shell')
                protreq(con, 'output', ' SHUTDOWN   - Shutdown the service')
                protreq(con, 'output', ' ABOUT      - About this software')
            elif data['data'].upper() == 'ABOUT':
                protreq(con, 'output', 'MS - by Till Vennefrohne 2023')
            elif data['data'].upper() == 'SHUTDOWN':
                os._exit(0)
            else:
                protreq(con, 'output', 'Unknown command. Type HELP')

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
                protreq(con, 'output', ' JOIN')
                protdisc(con)
            
            elif data['data'][0].upper() == 'JOIN':
                protreq(con, 'output', 'Shell. Type EXIT to leave')

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
     


def clientHandler(con, data):
       
        if data['method'] == 'output':
            out(data['data'])

        if data['method'] == 'input':
            protreq(con,'input',input())

        if data['method'] == 'disconnect':
            out("Disconnecting")
            #con.close()
            os._exit(0)

