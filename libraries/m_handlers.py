import m_ipc

def serverHandler(server, data):
        print("Server: " + str(data))
        server.send("Yop")        

def clientHandler(client, data):
        print("Client: " + str(data))

