import pygame

class GameCaller:
    """clase que modela las llamadas a los juegos"""
    def __init__(self):
        #constructor
        print("GameCaller Inicializado")
        self.__DbgMsg = True #Activar o desactivar mensajes de debug

    def GameCall(self,gameEP,MTMode = False):
        """M�todo que realiza la llamada al Entrypoint del juego. gameEP debe ser una instancia de Start o derivado. MTMode es un valor booleano que indica si la llamada se realiza en un nuevo Thread o no (Default: Falso)"""
        if MTMode:
            #Llamada MultiTheaded
            if self.__DbgMsg: 
                print("Llamada MT")
            try:
                GameThead = pygame.threads.Thread(gameEP.Go).start()
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
                    print("Excepci�n en juego, retornando")
                return -1

