import json
import time

#Create packet which can be sent through socket.
#If asbytes is false return packet as dictionary,


class Utilities():
    def __init__(self):
        self.token = None

    def setToken(self,token):
        self.token = token

    def createPacket(self,name='undefined-packet',data={},asbytes=True):
        packet = {
            'action':name,
            'data':data,
            'packet-created':time.time(),
            'token':self.token
        }
        
        if asbytes:
            return bytes(json.dumps(packet),"utf-8")
        return packet

    #Return string or dict version of the packet.
    def decodePacket(self,packet,asdict=True):
        packet = packet.decode('utf-8')
        if asdict:
            try:
                packet = json.loads(packet)
            except:
                print("Failed to decode packet")
                return False
        return packet

if __name__ == '__main__':
    ou = Utilities()
    p = ou.createPacket('auth',{
        'username':'cmdtvt',
        'password':'password'
    })

    print(p)

    ou.setToken("this is token")
    print(ou.decodePacket(ou.createPacket('auth',{
        'username':'cmdtvt',
        'password':'password'
    })))
    