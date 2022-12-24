## Python Socket Server & Client
This project is designed to siplify TCP server / client communication. Server and client can be easily implemented into needed project.

### Start a server
When starting a server Server() can be provided with host & port on default they are `127.0.0.1` and `25565`

    from pnetwork import coreserver
    s = coreserver.Server()
    s.start()

### Start a client
    from pnetwork import coreclient
    c = coreclient.Client()
    c.start()


### Basic packets
When sending packets to and from the server their type/name can be defined. Name of the packet defines what is done with the packet when it arrives to it's destination. 
You can create a packet with `createPacket()` function in both server and client.

#####  Example of creating a custom packet on the server side

    from network import coreserver
    
    s = coreserver.Server()
    s.start()
    
    s.createPacket("PACKETNAME",{
	    'example':"this is a message",
	    'data' : "this is also data"
    })
Create packet also packs in some extra identifying info that is automaticly sent with every packet. The "full" version of the above packet when receiving it would look like this. Your data will always be value of the data key.
##### Example of a full packet

    {
	    'action':[NAME OF THE PACKET],
	    'data': {
			'example':"this is a message",
			'data' : "this is also data"
		},
	    'packet-created':[WHEN PACKET WAS CREATED AS TIMESTAMP],
	    'token': [CONNECTION IDENTIFICATION TOKEN]
	 }


### Handle a custom packet
How do you react to a custom packet that you send through the network? This can be done by using the `bindAction` function.
##### Example of registering a new action

    from network import coreserver
    
    s = coreserver.Server()
    s.start()

    class  testAction(Bind):
	    def  __init__(self,name,*args):
		    super().__init__(name,*args)
		    self.test =  "test"
		    
		    
	    def  run(self,data="yeet"):
		    print(self.test)
		    

    s.bindAction("[PACKET NAME]",testAction("trigger test"))
    
If packet arrives with the name of `[PACKET NAME]` run function is ran from `testAction` class.

### Handshake
When client connects to server handshake packet is sent. When server recieves this packet the client is registered into server's memory and a unique token is sent back to the client. This token that is sent to client can be used to identify the packages that come from that spesific client. This is refered in code as `token`.
Server & Client store the connections as `Connection` objects that are stored in `self.clients`. With `Connection`  object you can send packet's to certain Client/Server.

If some other client get's it's hands on token of another client it can cause a lot of trouble. This token should NEVER be revealed to other client's.

(Token is currently created with `uuid4` on the server side this implementation can be changed later.)

### Connection object
Connection object can be used to talk with a connection. When new connection arrives a `Connection` object is created from it. When `startlisten` is called a thread is started that wait's for packet's for just that connection.
Packet can be sent to a connection with `sendPacket()` method.
##### Example of getting a client with token and sending a custom packet to it
to be added

### Encryption
#### Encryption is not implemented at the moment. Some features exist already in `onlineUtilities.py` but are not used

This system uses [PyPi RSA](https://pypi.org/project/rsa/) encryption.
Packets are not encryped by default. Functions `createPacket()` and `decodePacket()` only make sure that the data is sent in a readable format.
packet that is made with createPacket can be encrypted with `encryptPacket()` and decoded with `decryptPacket()`

To make encryption usable you need to call `createEncryptKeys()` from the `onlineUtilities.py` this create public and private key for the server. This same process needs to be done for the client also if using encryption.

### Coretools
Coretools is optional simple CLI for running basic commands on server/client. Pass CLI class a server / client instance / object and call `processCommand()` to start listening userinput in console. Type `help` to see list of available commands for coretools

    from pnetwork import coretools
    ct = coretools.CLI([CORESERVER/CLIENT INSTANCE],"[OPTIONAL DISPLAYNAME]")
    ct.processCommand()


(Coretools will be reworked at somepoint currently it's not that well implemented)
