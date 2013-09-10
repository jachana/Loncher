#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pygame
import multiprocessing
import ArcadeWatchdog
from StartBase import Start

class GameCaller:
    """clase que modela las llamadas a los juegos"""
    def __init__(self):
        """Constuye un nuevo GameCaller"""
        #constructor
        #Activar o desactivar mensajes de debug
        self.__DbgMsg = True 
        if self.__DbgMsg:
            print("GameCaller Inicializado")

    def DbgOut(self, Msg = "Debug Test"):
        """M�todo que permite imprimir mensajes de debug a consola cuando se activan estos mensajes"""
        if self.__DbgMsg:
            print(Msg)

    def GameCall(self,gameEP,MTMode = False):
        """M�todo que realiza la llamada al Entrypoint del juego. gameEP debe ser una instancia de Start o derivado. MTMode es un valor booleano que indica si la llamada se realiza en un nuevo Thread o no (Default: Falso)"""
        if MTMode:
            #Llamada MultiTheaded
            if self.__DbgMsg: 
                print("Llamada MT")
            try:
                #Ac� creamos los Threads para el juego y el m�dulo antihang, los iniciamos y esperamos el join.
                #@jheysen 9-9-13: Cambiado a Mutiprocessing porque as� hay terminate()
                GameThead = multiprocessing.Process(None,gameEP.Go,"Juego",None,None)
                GameThead.daemon = False #Nos aseguramos que Phyton no puede cerrar si el juego no ha cerrado
                GameThead.start()
                #Ahora ponemos a correr el antihang
                self.DbgOut("Creando Antihang")
                WD = ArcadeWatchdog.ArcadeWatchdog()
                WD.SetHGame(gameEP)
                WD.SetHGThread(GameThead)
                WDProc = multiprocessing.Process(None,WD.WDMain,"Antihang",None,None)
                WDProc.daemon = True #Este si es un daemon
                WDProc.start()
                self.DbgOut("Esperando fin del juego")
                GameThead.join()
                self.DbgOut("Juego finalizado correctamente, se�alando fin de antihang")
                #Una vez que termin� el juego, paramos el Watchdog
                WD.FlagKill()
                return 0
            except:
                return -1
        else:
            #Llamada dentro del mismo Thread
            #No hay llamada al m�dulo antihang porque ac� no hay como controlarlo.. as� que simplemente esperamos el retorno del m�todo.
            if self.__DbgMsg: 
                print("Llamada ST")
            ec = 0
            try:
                ec = gameEP.Go()
                return ec
            except:
                if self.__DbgMsg: 
                    print("Excepci�n en juego, retornando")
                return -1

