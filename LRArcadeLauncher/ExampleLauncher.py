from LRArcadeLauncher import GameCaller
from bh.test_pygame import MiJuego
def main():
    gc = GameCaller()
    juego = MiJuego()
    gc.GameCall(juego,True)

if __name__ == "__main__":
    print("Prueba de Lanzamiento de juego")
    main()
