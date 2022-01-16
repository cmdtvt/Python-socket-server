import socket
import onlineUtilities as ou

ip = "127.0.0.1"
port = 25565
#soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #socket.SOCK_DGRAM

p = ou.createPacket('auth',{
    'username':'dev',
    'password':'test'
})


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    s.sendall(p)
    data = s.recv(1024)

print('Received', ou.decodePacket(data))

