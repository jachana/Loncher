#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Adaptado desde ejemplo publicado por Daniel Fuentes B.
# Licencia: X11/MIT license http://www.opensource.org/licenses/mit-license.php
# http://pythonmania.wordpress.com/2010/03/25/tutorial-pygame-2-ventana-e-imagenes/
 
# ---------------------------
# Importacion de los modulos
# ---------------------------
 
import pygame
from pygame.locals import *
import sys
import os
import StartBase



#--------------------------------------------------------------
# Modulo heredado de StartBase requerido para iniciar el juego
#--------------------------------------------------------------
class MiJuego(StartBase.Start):
    def Go(self):
        main()
 
# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "bh"+os.path.pathsep+"imagenes"
SONIDO_DIR = "bh/sonidos"
 
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
 
 
def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except pygame.error, message:
        print "No se pudo cargar el sonido:", ruta
        sonido = None
    return sonido

class bala(pygame.sprite.Sprite):
    "Balas"
    def __init__(self,dmg,spdx,spdy):
        pygame.sprite.Sprite.__init__(self)
        print ("Bala creada")
        self.image = load_image("bala.png",IMG_DIR,True)
        self.rect = self.image.get_rect()
        self.speed = [spdx,spdy]
        self.dmg = dmg

    def colision(self, objetivo):
        "Detecta hits"
        if self.rect.colliderect(objetivo.rect):
            objetivo.hp = objetivo.hp - self.dmg
            objetivo.HitSound.play()

    def update(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery -= self.speed[1]

class jugador(pygame.sprite.Sprite):
    "Jugador"
    def __init__(self, *groups):
        return super(jugador, self).__init__(*groups)

    def __init__(self, hp):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
        self.image = load_image("nave.png",IMG_DIR,True)
        #self.HitSound = load_sound("hit.mp3",SONIDO_DIR)
        self.rect = self.image.get_rect()
        self.speed = [0,0]
        self.rect.centerx = SCREEN_WIDTH /2
        self.rect.centery = SCREEN_HEIGHT - 20

class jefe(pygame.sprite.Sprite):
    "Jefe y comportamiento"

    def __init__(self, hp):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
        self.image = load_image("jefe.png",IMG_DIR,True)
        #self.HitSound = load_sound("hit.mp3",SONIDO_DIR)
        self.rect = self.image.get_rect()
        self.speed = [0,0]
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = 100
        self.tickcount = 0

    def tick(self):
        "IA del jefe"
        self.tickcount += 1


# ------------------------------
# Funcion principal del juego
# ------------------------------

 
def main():
    pygame.init()
    pygame.mixer.init()
      
    
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BulletHell POC")
    fondo = load_image("0.jpg",IMG_DIR,False)

    #creo contenedores globales
    balas = []

    player = jugador(100)
    boss = jefe(10)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)
 
    # el bucle principal del juego
    while True:
        clock.tick(60)
        boss.tick()

        #Analísis de colisiones
        for b in balas[:]:
            b.colision(player)
            b.colision(boss)

        #Mover balas
        for b in balas[:]:
            b.update()

        #condiciones de fin
        if boss.hp <= 0:
           sys.exit(0)
        elif player.hp <= 0:
           sys.exit(0)
            
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    player.rect.centery -=5
                elif event.key == K_DOWN:
                    player.rect.centery +=5
                elif event.key == K_LEFT:
                    player.rect.centerx -= 5
                elif event.key == K_RIGHT:
                    player.rect.centerx += 5
                elif event.key == K_SPACE:
                    print ("Creando bala")
                    bb = bala(1,0,2)
                    bb.rect.centerx = player.rect.centerx
                    bb.rect.centery = player.rect.centery - 50
                    balas.append(bb)
                    #balas.append(bala(1,0,2))
                elif event.key == K_ESCAPE:
                    sys.exit(0)

        #Rendering
        screen.blit(fondo,(0,0))
        screen.blit(player.image,player.rect)
        screen.blit(boss.image,boss.rect)
        for b in balas:
            screen.blit(b.image,b.rect)
        pygame.display.flip()
 
 
if __name__ == "__main__":
    main()
