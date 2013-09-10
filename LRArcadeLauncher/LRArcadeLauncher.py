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
        """Método que permite imprimir mensajes de debug a consola cuando se activan estos mensajes"""
        if self.__DbgMsg:
            print(Msg)

    def GameCall(self,gameEP,MTMode = False):
        """Método que realiza la llamada al Entrypoint del juego. gameEP debe ser una instancia de Start o derivado. MTMode es un valor booleano que indica si la llamada se realiza en un nuevo Thread o no (Default: Falso)"""
        if MTMode:
            #Llamada MultiTheaded
            if self.__DbgMsg: 
                print("Llamada MT")
            try:
                #Acá creamos los Threads para el juego y el módulo antihang, los iniciamos y esperamos el join.
                #@jheysen 9-9-13: Cambiado a Mutiprocessing porque así hay terminate()
                self.DbgOut("[MTCALL]Creando proceso de juego")
                GameThead = multiprocessing.Process(None,gameEP.Go,"Juego",(),{})
                GameThead.daemon = False #Nos aseguramos que Phyton no puede cerrar si el juego no ha cerrado
                GameThead.start()
                self.DbgOut("[MTCALL]Proceso iniciado")
                #Ahora ponemos a correr el antihang
                self.DbgOut("[MTCALL]Creando Antihang")
                WD = ArcadeWatchdog.ArcadeWatchdog()
                WD.SetHGame(gameEP)
                WD.SetHGThread(GameThead)
                WDProc = multiprocessing.Process(None,WD.WDMain,"Antihang",(),{})
                WDProc.daemon = True #Este si es un daemon
                #WDProc.start()
                self.DbgOut("[MTCALL]Esperando fin del juego")
                GameThead.join()
                self.DbgOut("[MTCALL]Juego finalizado correctamente, señalando fin de antihang")
                #Una vez que terminó el juego, paramos el Watchdog
                WD.FlagKill()
                return 0
            except:
                #pass
                self.DbgOut("[MTCALL]Excepción no controlada")
                return -1
        else:
            #Llamada dentro del mismo Thread
            #No hay llamada al módulo antihang porque acá no hay como controlarlo.. así que simplemente esperamos el retorno del método.
            if self.__DbgMsg: 
                print("Llamada ST")
            ec = 0
            try:
                self.DbgOut("[STCALL]Iniciando juego")
                ec = gameEP.Go()
                self.DbgOut("[STCALL]Juego retorna normalmente")
                return ec
            except:
                if self.__DbgMsg: 
                    print("[STCALL]Excepción en juego, retornando")
                return -1

