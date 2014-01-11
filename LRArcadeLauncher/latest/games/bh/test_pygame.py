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
EPIC = True
 
# ------------------------------
# Funciones utiles
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

#--------------------------
# Entidades del juego
#--------------------------

#-------------------------------------------------------------

### Representa las balas que lanza el jefe
class bala(pygame.sprite.Sprite):
    "Balas"
    def __init__(self,x,y,spdx,spdy,timer,color):
        pygame.sprite.Sprite.__init__(self)
        print ("Bala creada")
        self.image = load_image("bala"+str(color)+".png",IMG_DIR,True)
        self.x = x
        self.y = y
        self.speed = [spdx,spdy]
        self.time = timer*60
        self.accel = [0,0]

    def colision(self, objetivo):
        pass ##TODO

    def absspeed(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)

    ##Actualiza la posicion de la bala segun sus parametros. Retorna True cuando se le acabo el tiempo.
    def update(self):
        self.x += self.speed[0]
        self.y -= self.speed[1]

        oldspd = self.absspeed()
        self.speed[0]+=self.accel[0]
        self.speed[1]+=self.accel[1]
        if(self.absspeed() > oldspd and self.absspeed()>5):
            self.speed[0]-=self.accel[0]
            self.speed[1]-=self.accel[1]
        
        
        self.time-=1
        if(self.time == 0):
            return True
        return False



#-----------------------------------------------------------------





### Representa al pleyer
class jugador(pygame.sprite.Sprite):
    "Jugador"
    def __init__(self, *groups):
        return super(jugador, self).__init__(*groups)

    def __init__(self):
        self.score = 0        
        pygame.sprite.Sprite.__init__(self)
        #Indica si el jugador esta disparando o no
        self.lazor = False
        #Cargamos el sprite del jugador
        self.image = load_image("nave.png",IMG_DIR,True)
        #Establecemos las coordenadas del jugador 
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH /2
        self.rect.centery = SCREEN_HEIGHT - 20
        #Establecemos los rectanguos que componen el laser
        self.laser = [Rect(self.rect.centerx-3,0,7,self.rect.centery),Rect(self.rect.centerx-2,0,5,self.rect.centery),Rect(self.rect.centerx-1,0,3,self.rect.centery),Rect(self.rect.centerx,0,1,self.rect.centery)]

    def checkdmg(self, boss):
        for b in boss.balas:
            if(math.sqrt((self.rect.centerx-b.x)*(self.rect.centerx-b.x)+(self.rect.centery+7-b.y)*(self.rect.centery+7-b.y))<8):
                return True
            if(math.sqrt((self.rect.centerx-b.x)*(self.rect.centerx-b.x)+(self.rect.centery+7-b.y)*(self.rect.centery+7-b.y))<16):
                self.score+=1
        return False

    ##Procesa el input
    def keyinput(self, key):

        #Si se esta aprentando espacio, disparar
        if(key.SPACE):
            if(not self.lazor):
                self.lazor = True
        else:
            if(self.lazor):
                self.lazor = False
        
        #velocidad del jugador
        s = 3
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
        #miau        


#--------------------------------------------------------------------

###Representa al jefazo y todo lo que le pertenece
class jefe(pygame.sprite.Sprite):
    "Jefe y comportamiento"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Establecemos el HP del jefe
        self.hp = 6000
        #Y la barra que lo representa
        self.hpbar = [Rect(20,20,600,2),Rect(20,22,600,1),Rect(20,23,600,1),Rect(20,24,600,1),Rect(20,25,600,1)]
        #Cargamos el sprite del jefe
        self.image = load_image("boss.png",IMG_DIR,True)
        #Y establecemos sus coordenadas iniciales
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = -201
        self.tickcount = 0
        #Creamos un contenedor para las balas que dispare el jefe
        self.balas = []
        self.routine = 1

    ##Dramatica entrada del jefe a la pantalla, avisa cuando esta en posicion
    def enter(self):
        self.rect.centery+=3
        
        if(self.rect.centery == 150):
            return True
        else:
            return False
    ##El jefe revisa si el laser del jugador le esta pegando    
    def checkdmg(self,player):
        #Si el jugador tiene el laser encendido y este esta en el camino del jefe
        if(player.lazor and self.rect.collidelist(player.laser)>=0):
            self.hp -= 1.5
            player.score +=1.5
            #Actualizamos la barra
            for bar in self.hpbar:
                bar.width = self.hp//10         

    ##El jefe hace algo segun en cuanto HP se encuentra
    def tick(self):
        
        #Actualizamos las balas en pantalla
        cont = 0
        while cont <len(self.balas):
            #Si la bala murio luego de actualizar su posicion
            if(self.balas[cont].update()):
                self.balas.pop(cont) #La eliminamos de la lista
            else:
                cont+=1 #Si no, pasamos a la bala siguiente


        #Segun que tan debil se encuentra, que es lo que hace
        if(self.hp > 5000):
            self.routine_1()
        elif(self.hp > 4000):
            self.routine_2()
        elif(self.hp > 3000):
            self.routine_3()
        elif(self.hp > 2000):
            self.routine_4()
        elif(self.hp > 1000):
            self.routine_5()
        else:
            self.routine_6()
            
    def routine_2(self):
        if(self.routine == 1):
            self.balas = []
            self.routine = 2
            self.tickcount = 0
            
        self.tickcount +=1
        a = 5
        r = 1
        spd = 4
        mu = self.tickcount*a
        x = self.rect.centerx+math.cos(mu)*r
        y = self.rect.centery-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,57,6)
        self.balas.append(bullet)        

    def routine_1(self):
        

        self.tickcount +=1
        a = 5
        r = 1
        spd = 3
        mu = math.sin(self.tickcount)*a
        x = self.rect.centerx+math.cos(mu)*r
        y = self.rect.centery-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,4,1)
        self.balas.append(bullet)

    def routine_4(self):
        if(self.routine == 2):
            self.balas = []
            self.routine = 3
            self.tickcount = 0
            
        self.tickcount +=1
        a = 25
        r = 260*math.sin(self.tickcount*math.pi/360)
        spd = 3
        mu = self.tickcount*a
        x = self.rect.centerx+math.cos(mu)*r
        y = self.rect.centery-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,7,10)
        self.balas.append(bullet)

    def routine_3(self):
        if(self.routine == 2):
            self.balas = []
            self.routine = 3
            self.tickcount = 0
            
        self.tickcount +=1
        a = 24
        r = math.sin(self.tickcount*math.pi/360)
        spd = 3
        mu = self.tickcount*a
        x = self.rect.centerx+math.cos(mu)*r
        y = self.rect.centery-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,4,10)
        self.balas.append(bullet)

        a = -24
        r = math.sin(self.tickcount*math.pi/360)
        spd = 3
        mu = self.tickcount*a
        x = self.rect.centerx+math.cos(mu)*r
        y = self.rect.centery-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,4,8)
        self.balas.append(bullet)

    def routine_5(self):
        pass
    def routine_6(self):
        pass
                
                
            


#-----------------------------------
# Clases de Utility
#-----------------------------------

###Clase encargada de revisar los eventos del teclado
class keyboard():

    ##Se establecen las teclas a las que le prestaremos atencion
    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.SPACE = False

    ##Revisa cuando se aprieta y cuando se suelta una tecla para recordar que teclas estan presionadas en que momento
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
            elif keydown.key == K_z:
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
            elif keyup.key == K_z:
                self.SPACE = False            

# ------------------------------
# Funcion principal del juego
# ------------------------------

 
def main():
    #Se inicializa la libreria
    pygame.init()
    pygame.mixer.init()

    global screen    
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
    pygame.display.set_caption("BulletHell POC")
    fondo = load_image("espeis.png",IMG_DIR,False)    

    #Instanciamos al jugador y al jefe
    player = jugador()
    boss = jefe()

    #?????????
    clock = pygame.time.Clock()    
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas (???)

    #Escondemos el mouse
    pygame.mouse.set_visible(False)

    #Establecemos los colores de los rectangulos que se dibujaran a mano (laser y barra de Hp del jefe)
    colorbarra = [Color(255,0,0,0),Color(220,0,0,0),Color(160,0,0,0),Color(100,0,0,0),Color(40,0,0,0)]
    lasercolor = [Color(0,0,255,0),Color(135,206,250,0),Color(255,255,255,0),Color(255,255,255,0)]

    #Creamos el teclado
    key = keyboard()




    
#-----------
# Epic Intro
#-----------

    #Se carga y reproduce la musica para la epic intro... epicamente
    pygame.mixer.music.load(os.path.join(SONIDO_DIR,"space_0.mp3"))
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(0)
    
    intro = 0
    #Epic intro.... BEGIN!    
    while EPIC:
        clock.tick(60)

        # Posibles entradas del teclado y mouse
        key.check()

        # Dejamos al jugador moverse y disparar... para que se acostumbre...
        player.keyinput(key)                   
        
        # Si hay que salirse nos salimos :c
        if len(pygame.event.get(pygame.QUIT))>0:
            quitgame(player.score)
            
        #Rendering
        screen.blit(fondo,(0,intro-360)) #Nos acercamos hacia el horizonte
        if(player.lazor):
            for l in range(4):
                screen.fill(lasercolor[l],player.laser[l]) 
        screen.blit(player.image,player.rect)
        screen.blit(boss.image,boss.rect)
        pygame.display.flip()

        #La magia de la intro va aqui
        fadeout = True
        if(intro == 360): ##Una vez terminamos de subir
            if(fadeout): #Desvanecemos la musica
                pygame.mixer.music.fadeout(1500)
                fadeout = False
            pass
            if(boss.enter()): #Y le decimos al jefazo que entre
                break
        else:
            intro += 2 #A que velocidad se scrollea la pantalla

#--------------------------------
 
    #Comienza la pelea.... MUSICA MAESTRO!
    pygame.mixer.music.load(os.path.join(SONIDO_DIR,"rail.ogg")) #Epic trax
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    
#----------
# Main Loop
#----------
    while True:
        clock.tick(60)
        boss.tick()

        #Analísis de colisiones
        boss.checkdmg(player)
        
        if(player.checkdmg(boss)):
            quitgame(player.score)
        
        #Condiciones de fin
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
        for b in boss.balas:
            screen.blit(b.image,(b.x-8,b.y-8))
        screen.blit(player.image,player.rect)
        screen.blit(boss.image,boss.rect)
        
        for i in range(5):
            screen.fill(colorbarra[i],boss.hpbar[i])        
        
        pygame.display.flip()

#------------------------------------------------------

def quitgame(score):    
    print("Puntaje obtenido: "+str(score))
    sys.exit(0)    
 
if __name__ == "__main__":
    main()
