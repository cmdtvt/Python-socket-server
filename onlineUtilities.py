from ast import match_case
import json
import time
import rsa
import errno

#Create packet which can be sent through socket.
#If asbytes is false return packet as dictionary,

#TODO: Move encryption methods to their own class and extend Utilities class with it.

class Utilities():
    def __init__(self):
        self.token = None
        self.useEncrypt = True

        #This might not be needed here because it might be smarter to store keys elsewhere.
        #self.publickeys = None
        self.own_publickey = None

        #We dont want the private key accidentaly leaking anywhere
        #so lets keep it private in this class
        self.__own_privatekey = None
        self.keystrength = 1024

        if self.useEncrypt:
            self.createEncryptKeys()

    def setToken(self,token:str):
        self.token = str(token)
        print("Token was changed to: "+self.token)

    def getToken(self,):
        return self.token

    def createPacket(self,name:str='undefined-packet',data:dict=None,asbytes:bool=True):
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
    def decodePacket(self,packet:dict,asdict:bool=True):
        packet = packet.decode('utf-8')
        if asdict:
            try:
                packet = json.loads(packet)
            except:
                print("Failed to decode packet")
                print(packet)
                return False
        return packet

    #Create own public and private keys.
    def createEncryptKeys(self,save:bool=True):
        if save:
            self.own_publickey, self.__own_privatekey = rsa.newkeys(self.keystrength)
        return self.own_publickey

    def encryptPacket(self,packet,publicKey:str):

        #TODO: Add the same loop thing from decryptPacket so we can encrypt many values easily.

        #rsa encrypt has max lenght it can encrypt.
        #to get past this we will only encrypt the important data not the whole packet.
        encToken = rsa.encrypt(packet["token"].encode(),self.__own_privatekey)
        packet["token"] = encToken

        encData = rsa.encrypt(str(packet["data"]).encode(),self.__own_privatekey)
        packet["data"] = encData

        
        return packet


    ## Having decryptableKeys as list might cause problems because the function can keep values inside the list in memory.
    def decryptPacket(self,packet:dict,decryptableKeys:list=[],privateKey=None):
        if privateKey == None:
            privateKey = self.__own_privatekey

        for k in decryptableKeys:
            packet[k] = rsa.decrypt(packet[k], privateKey).decode()

        return packet


    def NetworkErrorNotDefined(Error):
        pass
    

    #Returns True if client needs to restart
    def checkNetworkError(self,error):
        message = "Caught exception socket.error ["+str(error)+"] : "+str(errno.errorcode[error])
        shouldRestart = False
        match error:
            case errno.ECONNREFUSED:
                message += "Could not connect"

            case errno.ECONNRESET:
                message += "Connection reset"
                shouldRestart = True

            case _:
                #raise self.NetworkErrorNotDefined
                #print("Undefined network error: ["+str(error)+"]")
                pass

        print(message)
        return shouldRestart


    def test(self,):
        print("Test in online utilities was ran!")
        return "This is a test function!"




    def getMethods(self,):
        temp = {
            "createPacket": self.createPacket,
            "decodePacket": self.decodePacket,
            "processPacket": self.processPacket,
            "checkNetworkError": self.checkNetworkError,
            "test":self.test
        }
        return temp

        #Below code is start of an automatic way to fetch all metods.
        '''''
        methods = [func for func in dir(self) if callable(getattr(self, func))]
        temp_dict = {}
        for m in methods:
            temp_dict[m] = m
        return temp_dict
        '''''

        



#Handle encrypting strings and packets with rsa.
class Encryption():
    def __init__(self):
        pass
    
    def encrypt(self,):
        pass

    def decrypt(self,):
        pass
    
    def encryptPacket(self,packet,publicKey):
        pass

    def decryptPacket(self,packet,decryptableKeys=[],privateKey=None):
        pass





if __name__ == '__main__':
    ou = Utilities()
    publicK = ou.createEncryptKeys()
    p = ou.createPacket('auth',{
        'username':'cmdtvt',
        'password':'password'
    },False)
    

    '''
    
    ou.setToken("this is token")
    
    print(ou.decodePacket(ou.createPacket('auth',{
        'username':'cmdtvt',
        'password':'password'
    })))
    '''

    encr = ou.encryptPacket(p,publicK)
    print(encr)

    print("#############################")

    decr = ou.decryptPacket(encr,["token","data"])
    print(decr)

    methods = ou.getMethods()

    print(methods['test']())
    