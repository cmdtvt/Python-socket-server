import socket
from uuid import uuid4
import warnings
import actions

#Rename to connection
#TODO: Remove permission systems from here no need for them.
class Connection():
    def __init__(self,onlineUtilities,uuid,address,username,socket):
        self.uuid = uuid
        self.ip,self.port = address
        self.socket = socket
        self.username = username
        self.ou = onlineUtilities


        self.handShake()

    def disconnect(self,):
        self.socket.close()

    def handShake(self,):

        p = self.ou.createPacket('handShake',{
            'status':'success',
            'uuid': self.uuid
        })
        self.socket.send(p)


    def __str__(self):
        return str(self.username)
        
####FIXME: Remove server classs from extending actions.py
class Server(actions.Actions):
    def __init__(self,host='127.0.0.1',port=25565):
        super().__init__()
        self.host = host #rename to host
        self.port = port
        self.bufferSize = 1024

        #use socket.SOCK_DGRAM for udp socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.clients = {}
        self.actions = {}


    def start(self,):
        print("Server started")
        self.socket.listen()
        while True:
            print("Waiting for connections...")
            client,address = self.socket.accept()
            self.storeConnection(ou,str(uuid4()),address,None,client) 

            data = client.recv(self.bufferSize)
            self.processPacket(data,client,address)

    #TODO: Find a way to send passed args to function.
    def bindAction(self,action,func,*args):
        if action.startswith("Core"):
            warnings.warn("Warning: "+action+" bind might be overiding Core function bind")
        print("Created function bind for action: "+action)
        self.actions[action] = {"func":func,"args":args}

    def storeConnection(self,ou,uuid,address,username,socket): 
        self.clients[uuid] = Connection(ou,uuid,address,username,socket)
        print("Connection stored: "+str(len(self.clients)))
        return self.clients[uuid]

    def processPacket(self,packet,client,address=None):
        packet = self.decodePacket(packet)
        action = packet['action']
        data = packet['data']

        ip = None
        port = None

        if address != None:
            ip,port = address

        #FIXME: Does not read new bindAction format.
        if action in self.actions:
            temp_action = self.actions[action]
            temp = temp_action['func'](data,temp_action["args"])
            if temp is not None:
                client.send(temp)
        else:
            print("Action not found")


if __name__ == '__main__':
    s = Server()
    #s.bindAction("auth",s.ActionAuth,s.storeConnection)
    s.bindAction("listallclients",s.ListAllClients,s.clients)
    s.start()
