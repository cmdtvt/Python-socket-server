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
                    print("Error")





if __name__ == '__main__':
    s = Server()
    cli = coretools.CLI(s,"Server")


    class testAction(core.Bind):
        def __init__(self,name,*args):
            super().__init__(name,*args)
            self.test = "test"

        def run(self,data):
            print(self.test)

    class broadcast(core.Bind):
        def __init__(self,server,name="broadcast"):
            super().__init__(name)
            self.server = server
            

        def run(self,message="message undefined"):
            self.server.SendPacketForAll(self.server.createPacket("broadcast",message))

    s.bindAction("disconnect", testAction("disconnect"))
    s.bindAction("broadcast",broadcast(s))
    s.start()

    while True:
        cli.processCommand()

