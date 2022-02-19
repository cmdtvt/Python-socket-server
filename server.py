import socket
from uuid import uuid4
import warnings
#import onlineUtilities as ou
import actions


class Client():
    def __init__(self,uuid,ip,username):
        self.uuid = uuid
        self.ip = ip
        self.username = username
        self.permissions = {
            "admin":False
        }

    def checkPermission(self,name):
        if name in self.permissions:
            return self.permissions[name]
        return None

    def setPermission(self,name,value):
        self.permissions[name] = value
        if name in self.permissions:
            return True
        return False

    def __str__(self):
        return str(self.username)
        

class Server(actions.Actions):
    def __init__(self,ip='127.0.0.1',port=25565):
        super().__init__()
        self.ip = ip
        self.port = port
        self.bufferSize = 1024

        #use socket.SOCK_DGRAM for udp socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.bind((self.ip,self.port))
        self.clients = {}
        self.actions = {}


    def start(self,):
        print("Server started")
        self.socket.listen()
        while True:
            print("Waiting for connections...")
            client,address = self.socket.accept()
            data = client.recv(self.bufferSize)
            self.processPacket(data,client,address)

    def bindAction(self,action,func):
        if action.startswith("Core"):
            warnings.warn("Warning: "+action+" bind might be overiding Core function bind")
        print("Created function bind for action: "+action)
        self.actions[action] = func

    def storeClient(self,uuid,ip,username):
        temp = Client(uuid,ip,username)
        self.clients[uuid] = temp
        print(self.clients)

    def processPacket(self,packet,client,address=None):
        packet = self.decodePacket(packet)
        action = packet['action']
        data = packet['data']

        ip = None
        port = None

        if address != None:
            ip,port = address

        if action in self.actions:
            temp = self.actions[action](data,self.storeClient)
            if temp is not None:
                client.send(temp)
        else:

            if action == "CoreListClients":
                temp = ""
                for c in self.clients:
                    temp += c

                p = self.createPacket('ListClients',{
                    'clients':temp
                })
                client.send(p)
            else:
                print("Action not found")





if __name__ == '__main__':
    s = Server()
    s.bindAction("auth",s.ActionAuth)
    s.start()
