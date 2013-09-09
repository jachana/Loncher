import pygame
from StartBase import Start
class ArcadeWatchdog(object):
    """Clase que modela el módulo anti-hang para los juegos del launcher"""

    def __init__(self):
        """Incializa un watchdog, note que debe entregar el Handle a la clase start mediante SetHGame"""
        self.__KillFlag = False #Flag para que el main del WD termine
        self.__HGame = Start() #con esto el intérprete sabe que este parámetro siempre será un start
        self.__HGThread = pygame.threads.Thread() #Handle del Thread

    def WDMain(self):
        """Método principal de Watchdog"""
        PrevBeat = -1
        while True:
            if self.__HGame.GetWDMode:
                if PrevBeat == self.__HGame.GetPulse():
                    #Juego atorado...
                    #poner alguna forma de matar el Thread, pero oficial no hay...
                    pass
                else:
                    PrevBeat = self.__HGame.GetPulse()
            else:
                pass
            if self.__KillFlag:
                break


    def GetHGame(self):
        """Devuelve el Handle al Juego que cuida"""
        return self.__HGame
    def SetHGame(self,Game):
        """Establece el handle al Juego a Cuidar"""
        self.__HGame = Game
    def GetHGThread(self):
        """Obtiene Thread del juego"""
        return self.__HGThread
    def SetHGThread(self,t):
        """Establece cuál es el therad del juego que cuida"""
        self.__HGThread = t
    def FlagKill(self):
        """Indica que el watchdog debe finalizar en su próxima iteración"""
        self.__KillFlag = True


