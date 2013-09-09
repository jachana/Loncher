class Start:
    def __init__(self):
        self.__WDMode = False #uso de Watchdog, establece si se debe verificar o no
        self.__WDPulse = 0 #Uso de Watchdog, contador de ayuda
        pass
    def Go(self):
        try:
            pass
        except:
            pass

    def GetPulse(self):
        """retorna el valor del pulso"""
        return self.__WDPulse
    def SetPulse(self,p):
        """setea el pulso a un valor particular"""
        self.__WDPulse = p
    def Heartbeat(self):
        """Levanta flag de que el juego continúa vivo y no se ha quedado parado, es obligación llamarlo en cada frame"""
        self.SetPulse(self.GetPulse()+1)
    def GetWDMode(self):
        """Permite conocer si el juego indica que debe ser verificado por watchdog o no"""
        return self.__WDMode
    def SwitchWD(self):
        """Cambia el estado de Watchdog para este juego. Puede ser útil para evitar cierres mientras se obtienen recursos"""
        self.__WDMode = not self.__WDMode