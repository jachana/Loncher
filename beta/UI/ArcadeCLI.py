import system.game_man.gamelist as GL
import system.game_man.gameinfo as GI
import system.backend_facade as ABF

#Console UI
class ArcadeCLI:
    """Clase que modela una UI de consola para el arcade"""

    def __init__(self,backend):
        self._back = backend
        print("Aracde CLI 1.0 Initialized")
        print("There are "+str(len(self._back.getGameList().getList()))+" installed")
        print("Use list or l to get the codes")
        print("Use run CODE or r CODE to launch a game")
        print("Use help or h to read this again")
        print("Use quit or q to exit")

    def helpmsg(self):
        print("Use list or l to get the codes")
        print("Use run CODE or r CODE to launch a game")
        print("Use help or h to read this again")
        print("Use quit or q to exit")

    def listmsg(self):
        print(self._back.getGameList())

    def runmsg(self,code):
        print("[SYSTEM] Attempting to launch "+code)
        self._back.LoadGame(code)

    def go(self):
        buf = ""
        while buf.lower() != "quit" and buf.lower() != "q":
            buf = raw_input("User@Arcade>> ")
            lbuf = buf.lower()
            if lbuf == "help" or lbuf == "h":
                self.helpmsg()
            if lbuf == "list" or lbuf == "l":
                self.listmsg()
            if "run" in lbuf or "r" in lbuf:
                self.runmsg(buf.split(" ")[1])

    
