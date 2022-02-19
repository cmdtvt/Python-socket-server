from calendar import c
import onlineUtilities as ou
from uuid import uuid4

class Actions(ou.Utilities):

    def __init__(self):
        super().__init__()


    def ActionAuth(self,data,*args):
        print(args)
        storeClient = args[0]
        credentials = {"dev":"test","cmdtvt":"test2"}
        p = None
        if data['username'] in credentials and data['password'] == credentials[data['username']]:
            temp_uuid = str(uuid4())
            p = self.createPacket('auth',{
                'status':'success',
                'uuid': temp_uuid
            })
            
            storeClient(temp_uuid,0000,data['username'])
        else:
            p = self.createPacket('auth',{
                'status':'fail',
                'uuid': None
            })

        if p == None:
            return False
        return p
