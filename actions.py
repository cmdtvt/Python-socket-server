from calendar import c
import onlineUtilities as ou
from uuid import uuid4

class Actions(ou.Utilities):

    def __init__(self):
        super().__init__()

    ##FIXME: Pass storeClient as argument
    def ActionAuth(self,data,*args):
        storeConnection = args[0][0]
        #clientSocket = args[0][1]
        print(args)
        credentials = {"dev":"test","cmdtvt":"test2"}
        p = None
        if data['username'] in credentials and data['password'] == credentials[data['username']]:
            temp_uuid = str(uuid4())
            p = self.createPacket('auth',{
                'status':'success',
                'uuid': temp_uuid
            })
            
            storeConnection(temp_uuid,0000,data['username'],clientSocket)
        else:
            p = self.createPacket('auth',{
                'status':'fail',
                'uuid': None
            })

        if p == None:
            return False
        return p


    def ListAllClients(self,data,*args):
        temp = ""
        for c in self.clients:
            temp += c

        p = self.createPacket('ListClients',{
            'clients':temp
        })
        client.send(p)
