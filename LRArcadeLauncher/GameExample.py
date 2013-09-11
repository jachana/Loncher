#!/usr/local/bin/python

import StartBase

class MiJuego(StartBase.Start):
    
    def Go(self):
        #recordamos el WD parte desactivado, asi que aca se puede realizar carga de recursos sin miedo
        #Termina carga
        self.SwitchWD()
        #inicia la ejecucion
        self.Heartbeat()
        for i in range(0,100):
            print("[GAME]Iteracion"+str(i))
            self.Heartbeat() #Para que WD no mate al juego
        return 0