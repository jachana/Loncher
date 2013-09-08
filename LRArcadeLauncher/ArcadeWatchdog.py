from StartBase import Start
class ArcadeWatchdog(object):
    """Clase que modela el m�dulo anti-hang para los juegos del launcher"""

    def __init__(self):
        """Incializa un watchdog, note que debe entregar el Handle a la clase start mediante SetHGame"""
        self.__KillFlag = False #Flag para que el main del WD termine
        self.__HGame = Start() #con esto el int�rprete sabe que este par�metro siempre ser� un start
    def WDMain(self):
        """M�todo principal de Watchdog"""
        PrevBeat = -1
        while True:
            if self.__HGame.GetWDMode:
                pass
            else:
                pass
            if self.__KillFlag: break


    def GetHGame(self):
        """Devuelve el Handle al Juego que cuida"""
        return self.__HGame
    def SetHGame(self,Game):
        """Establece el handle al Juego a Cuidar"""
        self.__HGame = Game
    def FlagKill(self):
        """Indica que el watchdog debe finalizar en su pr�xima iteraci�n"""
        self.__KillFlag = True


