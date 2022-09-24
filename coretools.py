#### This file has code for taking user input and running client&server things with it.
#### Basicly this is very simple CLI



class CLI():
    def __init__(self,core):
        ### Takes in core class
        self.core = core
        print("###### CoreTools CLI ######")

    def processCommand(self,):
        command = str(input("Choose a command: "))
        command = command.split(" ")
        args = []
        
        for x in range(1, len(command)):
            args.append(command[x].replace(" ",""))


        match command[0].replace(" ",""):
            case "pingall":
                self.core.SendPacketForAll(self.core.createPacket("PING"))

            case "ping":
                self.core.SendPacket(command[1], self.core.createPacket("PING"))


            case "list":
                print(self.core.GetAllConnections())

            case "coninfo":
                uuid = input("Give connection uuid e for exit: ")
                if uuid == "e":
                    pass
                else:
                    print(self.core.GetConnection(uuid).GetRepersentation())

            case "disconnect":
                #self.core.SendPacket(command[1], self.core.createPacket("PING"))
                self.core.DisconnectConnection(command[1])

            case "disconnectrecent":
                print(self.core.DisconnectConnection(uuid))

            case "threads":
                t = self.core.GetThreadInfo()
                print(t)

            case "help":
                print('''
                pingall          (pings all clients)
                ping [UUID]      (ping client with UUID)
                list            (list all clients)
                coninfo [UUID]    (show info of connection)
                disconnect [UUID]  (disconnect a connection)
                disonnectrecent   (disconnect recent connection)
                threads         (show all threads that are running)
                help            (display this menu)
                ''')

            case "stop":
                print("Shutting down....")
            case _:
                print("unknown command")

