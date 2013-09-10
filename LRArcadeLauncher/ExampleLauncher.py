#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from LRArcadeLauncher import GameCaller
from GameExample import MiJuego

def main():
    gc = GameCaller()
    juego = MiJuego()
    gc.GameCall(juego,True)

if __name__ == "__main__":
    main()
