#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import StartBase

class MiJuego(StartBase.Start):
    
    def Go(self):
        #recordamos el WD parte desactivado, as� que ac� se puede realizar carga de recursos sin miedo
        #Termina carga
        self.SwitchWD()
        #inicia la ejecuci�n
        self.Heartbeat()
        for i in range(0,100):
            self.Heartbeat() #Para que WD no mate al juego
        return 0