import pygame
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
                GameThead = pygame.threads.Thread(None,gameEP.Go,"Juego",None,None,None)
                GameThead.setDaemon(False) #Nos aseguramos que Phyton no puede cerrar si el juego no ha cerrado
                GameThead.start()
                GameThead.join()
                return 0
            except:
                return -1
        else:
            #Llamada dentro del mismo Thread
            if self.__DbgMsg: 
                print("Llamada ST")
            ec = 0
            try:
                ec = gameEP.Go()
                return ec
            except:
                if self.__DbgMsg: 
                    print("Excepción en juego, retornando")
                return -1

