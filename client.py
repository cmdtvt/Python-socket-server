import socket
import onlineUtilities
import time
import errno
ip = "127.0.0.1"
port = 25565




class Client():
    def __init__(self,host='127.0.0.1',port=25565):
        super().__init__()
        print("Starting client")
        #rename to host
        self.host = host
        self.port = port
        self.bufferSize = 1024
        self.packetDelay = 5

        #Dont bind client connection. Just connect to server.
        #use socket.SOCK_DGRAM for udp socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ou = onlineUtilities.Utilities()
        self.ou.createEncryptKeys()

        self.connect()


    def connect(self,):
        while True:
            s = socket.socket()
            s.settimeout(5)
            try:
                self.socket.connect((self.host,self.port))
                p = self.ou.createPacket('handShake',{
                    'username' : 'dev',
                    'password' : 'test'
                })
                self.socket.send(p)
                print("Connected to server")
                break

            except socket.error as e:
                self.ou.checkNetworkError(e.errno)

    def start(self,):
        while True:
            try:
                time.sleep(self.packetDelay)
                data = self.socket.recv(self.bufferSize)
                print('Received', self.ou.decodePacket(data))
            except socket.error as e:
                if self.ou.checkNetworkError(e.errno):
                    print("Recieved command to shutdown")
                    break


if __name__ == '__main__':
    c = Client()
    c.start()
