#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import StartBase

class MiJuego(StartBase.Start):
    def __init__(self):
        return super(MiJuego, self).__init__()
    def Go(self):
        #recordamos el WD parte desactivado, así que acá se puede realizar carga de recursos sin miedo
        #Termina carga
        self.SwitchWD()
        #inicia la ejecución
        self.Heartbeat()
        for i in range(0,100):
            self.Heartbeat() #Para que WD no mate al juego
        return 0