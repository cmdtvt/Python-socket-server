import socket
from uuid import uuid4
import logging
import old.actions as actions
import core
import coretools

        
####FIXME: Remove server classs from extending actions.py
class Server(core.ComCore):
    def __init__(self,host='127.0.0.1',port=25565,bufferSize=1024):
        super().__init__(host,port,bufferSize)
        self.setToken(uuid4())
        self.socket.bind((self.host,self.port))

    ### Listen for new connections
    def listen(self,):
        self.socket.listen()
        while True:
            logging.info("Waiting for connections....")
            client,address = self.socket.accept()
            
            ### TODO: Find a way for this not to trigger everytime data is recieved.
            ### UUID of the connection is defined here and it's sent forwards by connection class.
            temp_token = str(uuid4())
            self.storeConnection(temp_token,address,None,client)
            self.GetConnection(temp_token).handShake(self.getToken())
            self.GetConnection(temp_token).startListen() #Start connections thread for listening packets
            





if __name__ == '__main__':
    s = Server()
    cli = coretools.CLI(s,"Server")


    class testAction(core.Bind):
        def __init__(self,name,*args):
            super().__init__(name,*args)
            self.test = "test"

        def run(self,data="yeet"):
            print(self.test)

    class broadcast(core.Bind):
        def __init__(self,server,name="broadcast"):
            super().__init__(name)
            self.server = server
            

        def run(self,message="message undefined"):
            self.server.SendPacketForAll(self.server.createPacket("broadcast",message))



    class handShake(core.Bind):
        def __init__(self,name,client,*args):
            super().__init__(name,*args)
            self.client = client
            logging.warning("Triggered handshake")

        def run(self,data,packet,socket):
            print("packet in run: "+str(packet))
            #self.client.setToken(data['uuid'])
            self.client.storeConnection(data['uuid'],socket.getpeername(),None,socket)



    s.bindAction("triggertest", testAction("trigger test"))
    #s.bindAction("handShake", handShake("handShake",s))
    #s.bindAction("broadcast",broadcast(s))
    s.start()

    while True:
        cli.processCommand()

