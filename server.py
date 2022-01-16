import socket
from uuid import uuid4
import onlineUtilities as ou

class Server():
    def __init__(self,ip='127.0.0.1',port=25565):
        self.ip = ip
        self.port = port
        self.bufferSize = 1024
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #socket.SOCK_DGRAM
        self.socket.bind((self.ip,self.port))

        self.clients = {}

    def start(self,):
        print("Server started")
        self.socket.listen()
        while True:
            print("Waiting for connections...")
            client,address = self.socket.accept()
            data = client.recv(self.bufferSize)
            self.processPacket(data,client,address)

    def processPacket(self,packet,client,address=None):
        print("Processing recieved data.")
        packet = ou.decodePacket(packet)
        print(packet)
        action = packet['action']
        data = packet['data']

        ip = None
        port = None
        if address != None:
            ip,port = address

        #Check if username and password is valid. Send client token which it can be identified by.
        if action == "auth":
            if data['username'] == "dev" and data['password'] == "test":
                print("Login valid")
                temp_uuid = str(uuid4())
                p = ou.createPacket('auth',{
                    'status':'success',
                    'uuid': temp_uuid
                })
            else:
                print("Login invalid")
                p = ou.createPacket('auth',{
                    'status':'fail',
                    'uuid': None
                })
            client.send(p)

        else:
            print("Action not defined")


if __name__ == '__main__':
    s = Server()
    s.start()