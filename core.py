#### This file has core parts of the network code.
#### Server & Client will extend this file to get all needed things.
import socket
import threading
import logging
import warnings
from uuid import uuid4
import time

#Basic connection object that stores socket and methods for managing it.
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

    ###TODO: If disconnect is called from connection class connection is still not removed from the client stiorage-
    def disconnect(self,):
        p = self.createPacket("disconnect",{
            "reason" : "connection disconnected"
        })
        self.sendPacket(p)
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


import onlineUtilities
import coreActions

class ComCore(onlineUtilities.Utilities):
    def __init__(self,host='127.0.0.1',port=25565,bufferSize=1024):
        super().__init__()
        self.host = host
        self.port = port
        self.bufferSize = bufferSize

        #use socket.SOCK_DGRAM for udp socket
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        
        self.clients = {}
        self.actions = {}
        self.loadCoreActions()

    def start(self,):
        thread_listen = threading.Thread(target=self.listen, args=())
        thread_listen.name = "thread_listen"
        thread_listen.start()

    ### Creates the metod binds for core actions.
    ### TODO: Possibly make this process automatic so only thing that needs to be done is to add new ones to coreActions.py
    def loadCoreActions(self,):
        print("Loading core actions...")
        self.bindAction("disconnect",self.DisconnectConnection,)
        pass




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

    def GetLatestConnection(self,):
        return list(self.clients.keys())[-1]

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


    def bindAction(self,action,func,*args):
        if action.startswith("Core"):
            warnings.warn("Warning: "+action+" bind might be overiding Core function bind")
        print("Created function bind for action: "+action)
        self.actions[action] = {"func":func,"args":args}


    #### Create a new connection object out of socket.
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

        if action in self.actions:
            temp_action = self.actions[action]
            temp = temp_action['func'](data,temp_action["args"])
            if temp is not None:
                client.send(temp)
        else:
            print("Action not found")
            print(packet)


    ### This is a dummy method
    def listen(self,*args):
        raise NotImplementedError()

    ### Start thread that listens to incoming connections & packets.
    ### TODO: Name this better maby?
    def start(self,):
        thread_listen = threading.Thread(target=self.listen, args=(), daemon=True)
        thread_listen.name = "thread_listen"
        thread_listen.start()