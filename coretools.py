#### This file has code for taking user input and running client&server things with it.
#### Basicly this is very simple CLI

import os
import sys
import threading

class CLI():
    def __init__(self,core,name="",ostype="windows"):
        ### Takes in core class
        self.core = core
        self.os = ostype
        print("###### CoreTools CLI | "+name+" ######")
        print("Mode: "+self.os)


    def startThreaded(self,):
        thread_listen = threading.Thread(target=self.processCommand, args=())
        thread_listen.name = "CoreTools CLI"
        thread_listen.start()


    def processCommand(self,):


        while True:
            command = str(input("Choose a command: "))
            command = command.split(" ")
            args = []
            
            for x in range(1, len(command)):
                args.append(command[x].replace(" ",""))

            try:
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
                        if command[1] == "self":
                            con1 = list(self.GetAllConnections().keys())[0]
                            print(con1)
                            #self.GetConnection().SendPacket(command[1], self.core.createPacket("PING"))
                        else:
                            self.core.DisconnectConnection(command[1])

                    case "dropall":
                        self.core.clients = {}

                    case "threads":
                        t = self.core.GetThreadInfo()
                        print(t)

                    case "broadcast":
                        pass

                    case "token":
                        print("Your token is: "+str(self.core.getToken()))

                    case "actions":
                        temp = self.core.actions.keys()
                        print(temp)

                    case "trigger":
                        name = command[1]
                        if name in self.core.GetActions():
                            self.core.GetActions()[name].run()
                        else:
                            print("No action found with name: "+str(name))

                    case "start":
                        print("Starting listening thread")
                        self.core.start()

                    case "clear":
                        if self.os == "windows":
                            os.system("cls")
                        elif self.os == "linux":
                            os.system("clear")
                        else:
                            print("unknown mode")

                    case "mode":
                        self.os = command[1]

                    case "help":
                        print('''
                        pingall          (pings all clients)
                        ping [UUID]      (ping client with UUID)
                        broadcast       (Send message to all clients)
                        list            (list all clients)
                        coninfo [UUID]    (show info of connection)
                        disconnect [UUID]  (disconnect a connection)
                        dropall         (Removes all clients from memory)
                        actions         (List all binded functions)
                        trigger         (Trigger a binded function)
                        threads         (show all threads that are running)
                        start           (Start connection listening thread)
                        clear           (Clear the screen)
                        mode [NAME]     (Change CLI mode)
                        help            (display this menu)
                        ''')

                    case "stop":
                        print("Shutting down....")
                        sys.exit()
                        break
                    case _:
                        print("unknown command")

            except:
                print("Error occured in command check your typing")

