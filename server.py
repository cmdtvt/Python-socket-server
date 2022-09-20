from calendar import c
import socket
from uuid import uuid4
import warnings
import threading
import logging
import actions
import random
import time

import onlineUtilities as ou

#Rename to connection
#TODO: Remove permission systems from here no need for them.
class Connection():
    def __init__(self,onlineUtilities,uuid,address,username,socket):
        self.uuid = uuid
        self.ip,self.port = address
        self.socket = socket
        self.username = username
        self.createPacket = onlineUtilities['createPacket']
        self.decodePacket = onlineUtilities['decodePacket']
        self.test = onlineUtilities['test']
        self.handShake()

    #Get all "important" information in dictionary
    def GetRepersentation(self,):
        temp = {
            "uuid" : self.uuid,
            "ip" : self.ip,
            "port" : self.port,
            "socket" : self.socket,
            "username" : self.username

        }
        return temp

    def disconnect(self,):
        p = self.createPacket("disconnect",{
            "reason" : "server disconnected"
        })
        self.socket.close()
        return True

    def handShake(self,):
        p = self.createPacket('handShake',{
            'status':'success',
            'uuid': self.uuid
        })
        self.sendPacket(p)

    #Checks if the client still responds if not drop the connection
    def isAlive(self,):
        p = self.createPacket('isAlive')
        self.sendPacket(p)


    def sendPacket(self,packet):
        self.socket.send(packet)


    def test(self,):
        print("This is a test method for connection class.")

        
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
        thread_listen = threading.Thread(target=self.listen, args=())
        thread_listen.name = "thread_listen"
        thread_listen.start()
        #self.mainLoop()



    ### Listen for new connections
    def listen(self,):
        self.socket.listen()
        while True:
            logging.info("Waiting for connections....")



            client,address = self.socket.accept()
            self.storeConnection(str(uuid4()),address,None,client)
            
            try:
                data = client.recv(self.bufferSize)
                self.processPacket(data,client,address)
                logging.info(str(data))
            except socket.error as e:
                if self.checkNetworkError(e.errno):
                    print("Recieved command to shutdown")
                    break



    def mainLoop(self,):
        print("running main loop")
        while True:
            time.sleep(10)
            p = self.createPacket("test",{"data":"this is test data"})
            #self.SendPacketForAll(p)
            print(self.GetRandomConnection().sendPacket(self.createPacket("HELLO")))
            print("Main runs")


    def SendPacket(self,uuid,packet):
        con = self.GetConnection(uuid)
        if con:
            con.sendPacket(packet)

    def SendPacketForAll(self,packet):
        for c in self.clients:
            self.clients[c].sendPacket(packet)
    
    def GetConnection(self,uuid):
        if uuid in self.clients:
            return self.clients[uuid]
        return None

    def GetAllConnections(self,):
        return self.clients

    ### Gets random connection. If no connection was found return False
    def GetRandomConnection(self,):
        temp = list(self.clients.keys())
        if len(temp) > 0:
            uuid = random.choice(temp)
            time.sleep(5)
            return self.clients[uuid]
        return False

    def DisconnectConnection(self,uuid):
        con = self.GetConnection(uuid)
        if con:
            con.disconnect()
            del self.clients[uuid]
            return True
        return False



    def GetThreadInfo(self,):
        threads = threading.enumerate()
        names = []
        for thread in threads:
            names.append(thread.name)

        temp = {
            "count" : len(threads),
            "names": names
        }

        return temp



    ### Method for testing threads.
    def threadTest(self,name="test"):
        waittime = random.randrange(4,20)
        logging.info("Thread %s: starting : %s", name,waittime)
        time.sleep(waittime)
        logging.info("Thread %s: finishing", name)


    def bindAction(self,action,func,*args):
        if action.startswith("Core"):
            warnings.warn("Warning: "+action+" bind might be overiding Core function bind")
        print("Created function bind for action: "+action)
        self.actions[action] = {"func":func,"args":args}


    def storeConnection(self,uuid,address,username,socket):
        self.clients[uuid] = Connection(self.getMethods(),uuid,address,username,socket)
        print("New connection stored with uuid: "+uuid+" | "+str(username)+" | Connections: "+str(len(self.clients)))
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


    while True:
        command = str(input("Choose a command: "))
        match command:
            case "pingall":
                s.SendPacketForAll(s.createPacket("PING"))


            case "list":
                print(s.GetAllConnections())

            case "connectioninfo":
                uuid = input("Give connection uuid e for exit: ")
                if uuid == "e":
                    pass
                else:
                    print(s.GetConnection(uuid).GetRepersentation())

            case "disconnect":
                uuid = input("Give connection uuid e for exit: ")
                if uuid == "e":
                    pass
                else:
                    print(s.DisconnectConnection(uuid))


            case "threads":
                t = s.GetThreadInfo()
                print(t)

            case "stop":
                print("Shutting down....")
                break

            case _:
                print("unknown command")

