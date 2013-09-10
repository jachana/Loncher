#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import multiprocessing
from StartBase import Start

class ArcadeWatchdog(object):
    """Clase que modela el m�dulo anti-hang para los juegos del launcher"""

    def __init__(self):
        """Incializa un watchdog, note que debe entregar el Handle a la clase start mediante SetHGame"""
        self.__KillFlag = False #Flag para que el main del WD termine
        self.__HGame = Start() #con esto el int�rprete sabe que este par�metro siempre ser� un start
        self.__HGThread = multiprocessing.Process() #Handle del Thread (Process)

    def WDMain(self):
        """M�todo principal de Watchdog"""
        PrevBeat = -1
        #GameCaller.DbgOut("[WD]Antihang iniciado")
        while True:
            if self.__HGame.GetWDMode:
                if PrevBeat == self.__HGame.GetPulse():
                    #Juego atorado...
                    #Trabajando con Multiprocessing, hay abort
                    #GameCaller.DbgOut("[WD]Abortando juego [HANG]")
                    self.__HGThread.terminate()
                    pass
                else:
                    #GameCaller.DbgOut("[WD]Continuando")
                    PrevBeat = self.__HGame.GetPulse()
            else:
                pass
            if self.__KillFlag:
                #GameCaller.DbgOut("[WD]Finalizando")
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
        """Establece cu�l es el therad del juego que cuida"""
        self.__HGThread = t
    def FlagKill(self):
        """Indica que el watchdog debe finalizar en su pr�xima iteraci�n"""
        self.__KillFlag = True


