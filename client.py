import socket
import onlineUtilities
import time
import threading

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

        self.actions = {}

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
        thread_listen = threading.Thread(target=self.listen, args=())
        thread_listen.name = "thread_listen"
        thread_listen.start()


    def listen(self,):
        while True:
            try:
                time.sleep(self.packetDelay)
                data = self.socket.recv(self.bufferSize)
                #print('Received', self.ou.decodePacket(data))
                self.processPacket(data)


            except socket.error as e:
                if self.ou.checkNetworkError(e.errno):
                    print("Recieved command to shutdown")
                    #self.connect()
                    break


    def bindAction(self,action,func,*args):
        if action.startswith("Core"):
            warnings.warn("Warning: "+action+" bind might be overiding Core function bind")
        print("Created function bind for action: "+action)
        self.actions[action] = {"func":func,"args":args}

    def processPacket(self,packet,address=None):
        packet = self.ou.decodePacket(packet)
        action = packet['action']
        data = packet['data']

        ip = None
        port = None

        if address != None:
            ip,port = address

        print(packet)
        #FIXME: Does not read new bindAction format.
        if action in self.actions:
            temp_action = self.actions[action]
            temp = temp_action['func'](data,temp_action["args"])
            if temp is not None:
                self.socket.send(temp)
        else:
            print("Action not found")

    def disconnect(self,*args):
        self.socket.close()
        print("Disconnected")


if __name__ == '__main__':
    c = Client()
    ##FIXME: Add checks that args are passed corretly and fucntion is not directly ran
    c.bindAction("disconnect",c.disconnect)
    c.start()

    while True:
        print("yeet")
        time.sleep(10)
