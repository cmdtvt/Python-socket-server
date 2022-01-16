import json
import time

#Create packet which can be sent through socket.
#If asbytes is false return packet as dictionary,
def createPacket(name='undefined-packet',data={},asbytes=True):
    packet = {
        'action':name,
        'data':data,
        'packet-created':time.time()
    }
    
    if asbytes:
        return bytes(json.dumps(packet),"utf-8")
    return packet

#Return string or dict version of the packet.
def decodePacket(packet,asdict=True):
    packet = packet.decode('utf-8')
    if asdict:
        try:
            packet = json.loads(packet)
        except:
            print("Failed to decode packet")
            return False
    return packet

if __name__ == '__main__':
    p = createPacket('auth',{
        'username':'cmdtvt',
        'password':'password'
    })

    print(p)

    print(decodePacket(createPacket('auth',{
        'username':'cmdtvt',
        'password':'password'
    })))
    