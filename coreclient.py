import socket
import time
import threading
import logging

ip = "127.0.0.1"
port = 25565


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
            s = socket.socket()
            s.settimeout(5)
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



    class testAction(core.Bind):
        def __init__(self,name,*args):
            super().__init__(name,*args)
            self.test = "test"

        def run(self,data):
            print(self.test)

    class handShake(core.Bind):
        def __init__(self,name,*args):
            super().__init__(name,*args)
            logging.warning("Triggered handshake")

        def run(self,packet):

            print(self.test())



    c = Client()
    cli = coretools.CLI(c,"Client")

    c.bindAction("disconnect", testAction("disconnect"))
    c.bindAction("handShake", handShake("handShake"))

    c.start(True)



    



    while True:
        cli.processCommand()

