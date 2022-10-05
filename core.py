### This file has core parts of the network code.
### Server & Client will extend this file to get all needed things.
import logging
import socket
import threading
import random
import warnings
from uuid import uuid4
import time

### Manages one connection from the socket
class Connection():
    def __init__(self,onlineUtilities,uuid,address,username,socket):
        self.uuid = uuid
        self.ip,self.port = address
        self.socket = socket
        self.username = username

        ### create & decodePacket need to be passed this way because onlineUtilities can have
        ### stored information about encryption keys etc...
        self.createPacket = onlineUtilities['createPacket']
        self.decodePacket = onlineUtilities['decodePacket']
        self.test = onlineUtilities['test']
        self.handShake()

    ### Get all "important" information in dictionary
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

    ### Send a response that handShake was successfull
    def handShake(self,):
        p = self.createPacket('handShake',{
            'status':'success',
            'uuid': self.uuid
        })
        self.sendPacket(p)

    ### Checks if the client still responds if not drop the connection
    def isAlive(self,):
        p = self.createPacket('isAlive')
        self.sendPacket(p)

    ### Send packet to the connection
    def sendPacket(self,packet):
        self.socket.send(packet)


    def test(self,):
        print("This is a test method for connection class.")



### Function that is "binded" extends this class.
class Bind():
    def __init__(self,name,*args):
        self.name = name
        self.args = args

    def run(self,data):
        raise NotImplementedError()

    def test(self,string="this is a test"):
        print(string)




import onlineUtilities
import coreActions

class ComCore(onlineUtilities.Utilities):
    def __init__(self,host='127.0.0.1',port=25565,bufferSize=1024):
        super().__init__()
        self.host = host
        self.port = port
        self.bufferSize = bufferSize
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.clients = {}
        self.actions = {}
        #self.loadCoreActions()

    ### Start a function that handles incoming connections.
    def start(self,useThreading=True):
        if useThreading:
            thread_listen = threading.Thread(target=self.listen, args=())
            thread_listen.name = "thread_listen"
            thread_listen.start()
        else:
            logging.warning("ComCore running in no threading mode.")
            self.listen()

    ### This is a dummy method
    def listen(self,*args):
        raise NotImplementedError()


    ### Creates the metod binds for core actions.
    def loadCoreActions(self,):
        print("Loading core actions...")
        self.bindAction("disconnect",self.DisconnectConnection,)


    ### Send packet to connection with certain UUID
    def SendPacket(self,uuid,packet):
        con = self.GetConnection(uuid)
        if con:
            con.sendPacket(packet)

    ### Send packet to all connections
    def SendPacketForAll(self,packet):
        for c in self.clients:
            self.clients[c].sendPacket(packet)
    
    ### Get connection with it's UUID
    def GetConnection(self,uuid):
        if uuid in self.clients:
            return self.clients[uuid]
        return None

    ### Get all connections
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

    ### Get the last connection in clients dictionary when it's converted to a list
    def GetLatestConnection(self,):
        return list(self.clients.keys())[-1]

    ### Disconnect a connection with it's UUID
    def DisconnectConnection(self,uuid):
        con = self.GetConnection(uuid)
        if con:
            con.disconnect()
            del self.clients[uuid]
            return True
        return False

    ### Get dictionary which has infomartion about threads
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


    #### Create a new connection object out of socket.
    def storeConnection(self,uuid,address,username,socket):
        self.clients[uuid] = Connection(self.getMethods(),uuid,address,username,socket)
        print("New connection stored with uuid: "+uuid+" | "+str(username)+" | Connections: "+str(len(self.clients)))
        return self.clients[uuid]

    ### Create a new bind to a function
    def bindAction(self,name,bind:Bind):
        self.actions[name] = bind

    ### Check if packet's action is found in self.actions. If so run the function.
    def processPacket(self,packet,client,address=None):
        logging.warning("Actions: "+str(self.actions))
        packet = self.decodePacket(packet)
        action = packet['action']
        data = packet['data']

        logging.warning("Searching for: "+str(action))

        ip = None
        port = None

        if address != None:
            ip,port = address

        if action in self.actions:
            temp_bind = self.actions[action]
            logging.warning(str(temp_bind))
            temp_bind.run(data)
        else:
            print("Action not found")
            print(packet)
