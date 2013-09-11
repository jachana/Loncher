import multiprocessing
class Start:
    def __init__(self):
        self.__WDMode = False #uso de Watchdog, establece si se debe verificar o no
        self.__WDPulse = 0 #Uso de Watchdog, contador de ayuda
        self.__HBQueue = multiprocessing.Queue() #Comunicacion
        pass
    def Go(self):
        try:
            return 0
        except:
            return -1

    def GetPulse(self):
        """retorna el valor del pulso"""
        return self.__WDPulse
    def SetPulse(self,p):
        """setea el pulso a un valor particular"""
        self.__WDPulse = p
    def Heartbeat(self):
        """Levanta flag de que el juego continua vivo y no se ha quedado parado, es obligacion llamarlo en cada frame"""
        self.SetPulse(self.GetPulse()+1)
        self.__HBQueue.put(self.GetPulse())
    def GetWDMode(self):
        """Permite conocer si el juego indica que debe ser verificado por watchdog o no"""
        return self.__WDMode
    def SwitchWD(self):
        """Cambia el estado de Watchdog para este juego. Puede ser util para evitar cierres mientras se obtienen recursos"""
        self.__WDMode = not self.__WDMode
    def SetQueue(self,cola):
        """Establece cola de comunicacion con antihang"""
        self.__HBQueue = cola