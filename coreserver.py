#from calendar import c
import socket
from uuid import uuid4
import warnings
import threading
import logging
import old.actions as actions
import random
import time

import core
import coretools

        
####FIXME: Remove server classs from extending actions.py
class Server(core.ComCore):
    def __init__(self,host='127.0.0.1',port=25565,bufferSize=1024):
        super().__init__(host,port,bufferSize)
        #self.host = host #rename to host
        #self.port = port
        #self.bufferSize = 1024

        #use socket.SOCK_DGRAM for udp socket
        #self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        #self.socket.bind((self.host,self.port))
        self.socket.bind((self.host,self.port))


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
                    #print("Recieved command to shutdown")
                    #break
                    print("Error")











if __name__ == '__main__':
    s = Server()
    cli = coretools.CLI(s)
    #s.bindAction("auth",s.ActionAuth,s.storeConnection)
    #s.bindAction("listallclients",s.ListAllClients,s.clients)
    s.start()


    while True:
        cli.processCommand()

