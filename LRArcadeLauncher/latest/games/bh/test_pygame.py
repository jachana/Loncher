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
import math
import random



#--------------------------------------------------------------
# Modulo heredado de StartBase requerido para iniciar el juego
#--------------------------------------------------------------
class MiJuego(StartBase.Start):
    def Go(self,services):
        main()
 
# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "./imagenes"
SONIDO_DIR = "./sonidos"
 
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
            objetivo.damage(self.dmg)
            return True
        return False
            
    def update(self):
        self.rect.centerx += self.speed[0]
        self.rect.centery -= self.speed[1]

class jugador(pygame.sprite.Sprite):
    "Jugador"
    def __init__(self, *groups):
        return super(jugador, self).__init__(*groups)

    def __init__(self):
        self.score = 0
        pygame.sprite.Sprite.__init__(self)
        self.lazor = False
        self.image = load_image("nave.png",IMG_DIR,True)
        self.HitSound = load_sound("hit.mp3",SONIDO_DIR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH /2
        self.rect.centery = SCREEN_HEIGHT - 20
        
        self.laser = [Rect(self.rect.centerx-3,0,7,self.rect.centery),Rect(self.rect.centerx-2,0,5,self.rect.centery),Rect(self.rect.centerx-1,0,3,self.rect.centery),Rect(self.rect.centerx,0,1,self.rect.centery)]

    def damage(self, dmg):
        pass

    def keyinput(self, key):
        #velocidad del jugador
        s = 6
        #velocidad diagonal
        ds = math.cos(math.pi/4)*s

        #Coordenadas anteriores por si se sale de la pantalla

        oldx = self.rect.centerx
        oldy = self.rect.centery

        #Movemos la nave segun que tecla esta presionada
        
        if(key.UP):
            if(key.DOWN):
                pass
            elif(key.LEFT):
                self.rect.centery-=ds
                self.rect.centerx-=ds
            elif(key.RIGHT):
                self.rect.centery-=ds
                self.rect.centerx+=ds
            else:
                self.rect.centery-=s
                
        elif(key.DOWN):

            if(key.LEFT):
                self.rect.centerx-=ds
                self.rect.centery+=ds
            elif(key.RIGHT):
                self.rect.centerx+=ds
                self.rect.centery+=ds
            else:
                self.rect.centery+=s
                
        elif(key.LEFT):
            if(key.RIGHT):
                pass
            else:
                self.rect.centerx-=s
        elif(key.RIGHT):
            self.rect.centerx += s

        #Si la nave salio de la pantalla con ese movimiento... el movimiento se cancela
        if not screen.get_rect().contains(self.rect):
            self.rect.centerx = oldx
            self.rect.centery = oldy

        #Actualizamos la posicion del laser
        self.laser[0].x = self.rect.centerx-3
        self.laser[0].height = self.rect.centery
        self.laser[1].x = self.rect.centerx-2
        self.laser[1].height = self.rect.centery
        self.laser[2].x = self.rect.centerx-1
        self.laser[2].height = self.rect.centery
        self.laser[3].x = self.rect.centerx
        self.laser[3].height = self.rect.centery
        

        #Si se esta aprentando espacio, disparar
        if(key.SPACE):
            self.lazor = True
        else:
            self.lazor = False
            
    

class jefe(pygame.sprite.Sprite):
    "Jefe y comportamiento"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 6000
        self.hpbar = [Rect(20,20,600,2),Rect(20,22,600,1),Rect(20,23,600,1),Rect(20,24,600,1),Rect(20,25,600,1)]
        self.image = load_image("jefe.png",IMG_DIR,True)
        self.HitSound = load_sound("hit.mp3",SONIDO_DIR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = -201
        self.tickcount = 0

    def enter(self):
        self.rect.centery+=3
        
        if(self.rect.centery == 150):
            return True
        else:
            return False
        
    def checkdmg(self,player):
        if(player.lazor and self.rect.collidelist(player.laser)>=0):
            self.hp -= 2
            player.score +=2
            for bar in self.hpbar:
                bar.width = self.hp//10         

    def tick(self):
        "IA del jefe"
        self.tickcount += 1


class keyboard():

    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.SPACE = False

    def check(self):
        keydowns = pygame.event.get(pygame.KEYDOWN)
        keyups = pygame.event.get(pygame.KEYUP)

        for keydown in keydowns:

            if keydown.key == K_ESCAPE:
                quitgame(":(")
            elif keydown.key == K_UP:
                self.UP = True
            elif keydown.key == K_DOWN:
                self.DOWN = True
            elif keydown.key == K_LEFT:
                self.LEFT = True
            elif keydown.key == K_RIGHT:
                self.RIGHT = True
            elif keydown.key == K_SPACE:
                self.SPACE = True

        for keyup in keyups:

            if keyup.key == K_UP:
                self.UP = False
            elif keyup.key == K_DOWN:
                self.DOWN = False
            elif keyup.key == K_LEFT:
                self.LEFT = False
            elif keyup.key == K_RIGHT:
                self.RIGHT = False
            elif keyup.key == K_SPACE:
                self.SPACE = False            

# ------------------------------
# Funcion principal del juego
# ------------------------------

 
def main():
    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(os.path.join(SONIDO_DIR,"space_0.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(0) 


    global screen    
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
    pygame.display.set_caption("BulletHell POC")
    fondo = load_image("espeis.png",IMG_DIR,False)

    #creo contenedores globales
    balas = []

    player = jugador()
    boss = jefe()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    
    colorbarra = [Color(255,0,0,0),Color(220,0,0,0),Color(160,0,0,0),Color(100,0,0,0),Color(40,0,0,0)]
    lasercolor = [Color(0,0,255,0),Color(135,206,250,0),Color(255,255,255,0),Color(255,255,255,0)]

    #Creamos el teclado
    key = keyboard()

    
    #bucle de introduccion
    intro = 0
    while True:
        clock.tick(60)

        #Mover balas
        for b in balas[:]:
            b.update()

        # Posibles entradas del teclado y mouse
        key.check()

        #El player actua segun el input
        player.keyinput(key)                   
        
        
        if len(pygame.event.get(pygame.QUIT))>0:
            sys.exit(0)
            
        #Rendering
        screen.blit(fondo,(0,intro-360))
        if(player.lazor):
            for l in range(4):
                screen.fill(lasercolor[l],player.laser[l])
        screen.blit(player.image,player.rect)
        screen.blit(boss.image,boss.rect)
        for b in balas:
            screen.blit(b.image,b.rect)
        pygame.display.flip()

        fadeout = True
        if(intro == 360):
            if(fadeout):
                pygame.mixer.music.fadeout(1500)
                fadeout = False
            pass
            if(boss.enter()):
                break
        else:
            intro += 0.5
 
    #Comienza la pelea.... MUSICA MAESTRO!
    pygame.mixer.music.load(os.path.join(SONIDO_DIR,"rail.ogg"))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    
    # el bucle principal del juego: 
    while True:
        clock.tick(60)
        boss.tick()

        #Analísis de colisiones
        boss.checkdmg(player)
        
        for b in balas:
            if(b.colision(player)):
                pass
            if(b.colision(boss)):
                pass

        #Mover balas
        for b in balas:
            b.update()

        #condiciones de fin
        if boss.hp <= 0:            
            quitgame(player.score)
            
        #Posibles entradas del teclado y mouse
        key.check()

        #El player actua segun el input
        player.keyinput(key)
                    
        
        #Si se le indica al juego que ya no mas... ya no mas!
        if len(pygame.event.get(pygame.QUIT))>0:
            quitgame(player.score)

        #Rendering
        screen.blit(fondo,(0,0))
        if(player.lazor):
            for l in range(4):
                screen.fill(lasercolor[l],player.laser[l])
        screen.blit(player.image,player.rect)
        screen.blit(boss.image,boss.rect)
        for b in balas:
            screen.blit(b.image,b.rect)
        for i in range(5):
            screen.fill(colorbarra[i],boss.hpbar[i])
        
        
        pygame.display.flip()

def quitgame(score):
    


    
    print("Puntaje obtenido: "+str(score))
    sys.exit(0)    
 
if __name__ == "__main__":
    main()
