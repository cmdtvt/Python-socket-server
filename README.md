## Python Socket Server & Client
This project is designed to siplify TCP server / client communication. Server and client can be easily implemented into needed project.
### Start a basic server
When starting a server Server() can be provided with host & port on default they are `127.0.0.1` and `25565`

    import server
    s = Server()
    s.start()

### Start a basic client
(Documentation to be added because of the constant changes to the structure of the code)

### Basic packets
When sending packets to and from the server their type or name can be defined. Name of the packet defines what is done with it when it arrives. If this name starts with Core they are "hard coded" functions that run something quite "low level" on the server. For example returning list of all connected clients.
You can create a packet with `onlineUtilities.py` server and client files use this automaticly so nothing weird needed.

Example of creating a custom packet
(This can be later made directly from the server object and sent)

    import onlineUtilities as ou

    ou.createPacket("PACKETNAME",{
	    'example':"this is a message",
	    'data' : "this is also data"
    })
Create packet also packs in some information that is sent on every packet. The "full" version of the above packet when receiving it would look like this. Your data will always be value of the data key.

    {
	    'action':[NAME OF THE PACKET],
	    'data': {
			'example':"this is a message",
			'data' : "this is also data"
		},
	    'packet-created':[WHEN PACKET WAS CREATED AS TIMESTAMP],
	    'token': [CONNECTION IDENTIFICATION TOKEN]
	 }

### Handshake
When client connects to the server the first time server expects a handshake packet. Packet should have name handShake and optionaly username and password can be provided. (Username & password check not implemented)

    import onlineUtilities as ou

    ou.createPacket("handShake",{
	    'username':"demo",
	    'password' : "test"
    })
After sending this packet to the server, the server sends back packet with identification token that should be sent along with every packet.

Also server stores the client as `Connection` to the server (This is done automaticly in the back).
(all connections are stored in `self.clients` on the server)

### Encryption
(Encryption is not fully implemented as automatic yet but it can be manyaly used at the moment)
This system uses [PyPi RSA](https://pypi.org/project/rsa/) encryption.
Packets are not encryped by default. Functions `createPacket()` and `decodePacket()` only make sure that the data is sent in a readable format.
packet that is made with createPacket can be encrypted with `encryptPacket()` and decoded with `decryptPacket()`

To make encryption usable you need to call `createEncryptKeys()` from the `onlineUtilities.py` this create public and private key for the server. This same process needs to be done for the client also if using encryption.
