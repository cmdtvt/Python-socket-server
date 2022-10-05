import socket
import time
import threading
import logging
import core
import coretools

class Client(core.ComCore):
    def __init__(self,host='127.0.0.1',port=25565,bufferSize=1024):
        super().__init__(host,port,bufferSize)
        self.socket.connect((self.host,self.port))
        self.packetDelay = 5

    def listen(self,):
        ###TODO: check if socket is still active.
        while True:
            try:
                time.sleep(self.packetDelay)
                data = self.socket.recv(self.bufferSize)
                print('Received', self.decodePacket(data))
                self.processPacket(data,self.socket)

            except socket.error as e:
                if self.checkNetworkError(e.errno):
                    print("Recieved command to shutdown")
                    break
    def connect(self,):
        while True:
            try:
                self.socket.connect((self.host,self.port))
                p = self.createPacket('handShake',{
                    'username' : 'dev',
                    'password' : 'test'
                })
                self.socket.send(p)
                print("Connected to server")
                break

            except socket.error as e:
                self.checkNetworkError(e.errno)


if __name__ == '__main__':


    ### TODO: Move classes from here to actions file.

    class handShake(core.Bind):
        def __init__(self,name,client,*args):
            super().__init__(name,*args)
            self.client = client
            logging.warning("Triggered handshake")

        def run(self,data,packet,socket):
            print("packet in run: "+str(packet))
            if(data['status']=="success"):
                print(socket)

                self.client.setToken(data['uuid'])
                self.client.storeConnection(data['remoteToken'],socket.getpeername(),None,socket)
            else:
                print("handShake returned status : "+str(data['status']))


    c = Client()
    cli = coretools.CLI(c,"Client")
    c.bindAction("handShake", handShake("handShake",c))

    c.start(True)


    while True:
        cli.processCommand()

