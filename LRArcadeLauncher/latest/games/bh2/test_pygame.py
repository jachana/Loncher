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
import string



#--------------------------------------------------------------
# Modulo heredado de StartBase requerido para iniciar el juego
#--------------------------------------------------------------
class MiJuego(StartBase.Start):
    def Go(self,services):
        #almacenamos el servicio para uso posterior
        global servicio
        try:
            servicio = services.getService("HighscoreService")
        except:
            pass
        main()
 
# -----------
# Constantes
# -----------
 
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "./imagenes"
SONIDO_DIR = "./sonidos"
EPIC = True
GOD = False
 
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
        self.image = load_image("bala"+str(color)+".png",IMG_DIR,True)
        self.x = x
        self.y = y
        self.speed = [spdx,spdy]
        self.time = timer*60
        self.accel = [0,0]
        self.max = 5

    def absspeed(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)

    ##Actualiza la posicion de la bala segun sus parametros. Retorna True cuando se le acabo el tiempo.
    def update(self):
        self.x += self.speed[0]
        self.y -= self.speed[1]

        oldspd = self.absspeed()
        self.speed[0]+=self.accel[0]
        self.speed[1]+=self.accel[1]
        if(self.absspeed() > oldspd and self.absspeed()>self.max):
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
        self.normal = load_image("nave.png",IMG_DIR,True)
        self.focus = load_image("shipfocus.png",IMG_DIR,True)
        #Inicialmente no esta enfocando
        self.speed = 6
        self.dmg = 0.5
        self.focused = False
        self.image = self.normal        
        #Establecemos las coordenadas del jugador 
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH /2
        self.rect.centery = SCREEN_HEIGHT - 20
        #Establecemos los rectanguos que componen el laser
        self.laser = [Rect(self.rect.centerx-3,0,7,self.rect.centery),Rect(self.rect.centerx-2,0,5,self.rect.centery),Rect(self.rect.centerx-1,0,3,self.rect.centery),Rect(self.rect.centerx,0,1,self.rect.centery)]

    def checkdmg(self, boss):
        for b in boss.balas:
            if(math.sqrt((self.rect.centerx-b.x)*(self.rect.centerx-b.x)+(self.rect.centery+7-b.y)*(self.rect.centery+7-b.y))<10):
                return True
            if(math.sqrt((self.rect.centerx-b.x)*(self.rect.centerx-b.x)+(self.rect.centery+7-b.y)*(self.rect.centery+7-b.y))<18):
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

        #Si esta enfocando, enfocar
        if(key.SHIFT):
            if(not self.focused):
                self.focused = True
                self.image = self.focus
                self.speed /= 2
                self.dmg *= 2
        else:
            if(self.focused):
                self.focused = False
                self.image = self.normal
                self.speed *= 2
                self.dmg /= 2
        
        #velocidad diagonal
        ds = math.cos(math.pi/4)*self.speed

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
                self.rect.centery-=self.speed
                
        elif(key.DOWN):

            if(key.LEFT):
                self.rect.centerx-=ds
                self.rect.centery+=ds
            elif(key.RIGHT):
                self.rect.centerx+=ds
                self.rect.centery+=ds
            else:
                self.rect.centery+=self.speed
                
        elif(key.LEFT):
            if(key.RIGHT):
                pass
            else:
                self.rect.centerx-=self.speed
        elif(key.RIGHT):
            self.rect.centerx += self.speed

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
        #Cargamos un efecto de sonido
        self.endcard = load_sound("se_tan02.wav",SONIDO_DIR)
        self.endcard.set_volume(0.5)
        self.endcardchannel = pygame.mixer.Channel(2)        
        #Creamos un contenedor para las balas y minions que genere el jefe
        self.balas = []
        self.minions = []
        self.routine = 1
        self.flag = False

    ##Dramatica entrada del jefe a la pantalla, avisa cuando esta en posicion
    def enter(self):
        self.rect.centery+=3
        
        if(self.rect.centery == 99):
            return True
        else:
            return False
    ##El jefe revisa si el laser del jugador le esta pegando    
    def checkdmg(self,player):
        #Si el jugador tiene el laser encendido y este esta en el camino del jefe
        if(player.lazor and self.rect.collidelist(player.laser)>=0):
            self.hp -= player.dmg
            #El jugador gana mas puntos si le pega al jefe sin enfocar
            player.score += 147
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


    def change_routine(self,ID):
        if(self.routine == ID-1):
            self.balas = []
            self.minions = []
            self.routine = ID
            self.tickcount = 0
            self.endcardchannel.play(self.endcard)
            
    def routine_1(self):
            
        self.tickcount +=1
        a = 5
        r = 1
        spd = 4
        mu = self.tickcount*a
        x = self.rect.centerx-10+math.cos(mu)*r
        y = self.rect.centery+50-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,4,6)
        self.balas.append(bullet)        

    def routine_2(self):
        
        self.change_routine(2)
            
        self.tickcount +=1
        a = 5
        r = 1
        spd = 4
        mu = self.tickcount*a
        x = self.rect.centerx-10+math.cos(mu)*r
        y = self.rect.centery+50-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,5,14)
        bullet.accel = [0,-0.1]
        self.balas.append(bullet)

    def routine_3(self):
        self.change_routine(3)
            
        self.tickcount +=1
        a = 24
        r = math.sin(self.tickcount*math.pi/360)
        spd = 3
        mu = self.tickcount*a
        x = self.rect.centerx-10+math.cos(mu)*r
        y = self.rect.centery+50-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,4,10)
        self.balas.append(bullet)

        a = -24
        r = math.sin(self.tickcount*math.pi/360)
        spd = 3
        mu = self.tickcount*a
        x = self.rect.centerx-10+math.cos(mu)*r
        y = self.rect.centery+50-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,4,8)
        self.balas.append(bullet)

    def routine_4(self):
        self.change_routine(4)

        a = 25
        r = 260*math.sin(self.tickcount*math.pi/360)
        spd = 3
        mu = self.tickcount*a

        if(len(self.minions)>0):
            self.minions[0].radius = 260*math.sin(self.tickcount*math.pi/360)
            self.minions[0].update(self.rect.centerx-10,self.rect.centery+50-20)
        else:
            mi = minion(self.rect.centerx,self.rect.centery-20,mu,100,25,5)            
            self.minions.append(mi)
            
        self.tickcount +=1
        
        x = self.rect.centerx-10+math.cos(mu)*r
        y = self.rect.centery+50-math.sin(mu)*r-20
        spdy = spd*math.sin(mu)
        spdx = spd*math.cos(mu)
        bullet = bala(x,y,spdx,spdy,7,10)
        self.balas.append(bullet)

    

    def routine_5(self):
        self.change_routine(5)

        
        
        if(len(self.minions) > 0):
            for m in self.minions:
                spdx = self.rect.centerx-10
                spdy = self.rect.centery+30
                m.update(self.rect.centerx-10,self.rect.centery+30)

                spdx-= m.x
                spdy-= m.y

                mod = math.sqrt((spdx)**2+(spdy)**2)

                spdx /= mod
                spdy /= mod
                mult = 2
                bullet = bala(m.x,m.y,-spdx*mult,spdy*mult,4,5)
                self.balas.append(bullet)
        else:
            n = 3
            for i in range(n):
                mi = minion(self.rect.centerx-10,self.rect.centery+30,(2*math.pi/n)*i,1,math.pi/30,2)
                mi.accel = math.pi/4000
                self.minions.append(mi)     

        self.tickcount +=1
        
    def routine_6(self):
        self.change_routine(6)

        if(len(self.minions) > 0):
            for m in self.minions:
                #Primero enviamos a los minions a rodear al jugador
                if(not self.flag):
                    m.radius = self.tickcount*3
                    m.update(self.rect.centerx,self.rect.centery+self.tickcount)

                    if(self.tickcount > 180):
                        self.flag = True
                else:
                    spdx = self.rect.centerx
                    spdy = self.rect.centery + 180                  

                    m.update(self.rect.centerx,self.rect.centery+180)

                    spdx-= m.x
                    spdy-= m.y

                    mod = math.sqrt((spdx)**2+(spdy)**2)

                    spdx /= mod
                    spdy /= mod
                    mult = 25
                    bullet = bala(m.x,m.y,-spdx*mult,spdy*mult,0.3,16)
                    self.balas.append(bullet)

                    if(m.radius > 35):
                        m.radius-=2
                    elif(self.tickcount%15 == 0):
                        global player
                        spdx = player.rect.centerx-self.rect.centerx
                        spdy = player.rect.centery-self.rect.centery

                        mod = math.sqrt((spdx)**2+(spdy)**2)

                        spdx /= mod
                        spdy /= mod

                        mult = 3
                        bullet = bala(self.rect.centerx,self.rect.centery,spdx*mult,-spdy*mult,2,15)
                        self.balas.append(bullet)
                    
                    
                        
        else:
            n = 10
            for i in range(n):
                k = -1
                if(i%2==0):
                    k*=-1
                
                mi = minion(self.rect.centerx,self.rect.centery,(2*math.pi/n)*i,0,math.pi/140*k,0)
                self.minions.append(mi)     

        self.tickcount += 1
        
        
  
                
                
#-------------------------------------------------------------

### Representa los minion que invoca el jefe
class minion(pygame.sprite.Sprite):
    
    def __init__(self,cx,cy,a,r,spd,color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = load_image("bala"+str(color%8 + 17)+".png",IMG_DIR,True)
        self.radius = r
        self.alpha = a
        self.cx = cx
        self.cy = cy
        self.x = self.cx + self.radius*math.cos(self.alpha)
        self.y = self.cy - self.radius*math.sin(self.alpha)
        self.speed = spd
        self.accel = 0

    ##Actualiza la posicion del minion segun sus parametros.
    def update(self,x,y):
        self.cx = x
        self.cy = y
        self.speed+=self.accel
        self.alpha+=self.speed
        self.x = self.cx + self.radius*math.cos(self.alpha)
        self.y = self.cy - self.radius*math.sin(self.alpha)
        

    


#-----------------------------------
# Clases de Utility
#-----------------------------------


###Clase encargada de manejar los puntajes
class score():

    def __init__(self,scorum,isplayer):
        self.isplayer = isplayer
        split = scorum.split(" ")
        let = split[0]
        self.initials=[let[0],let[1],let[2]]
        self.score = int(split[1])

    def __str__(self):
        num = str(self.score)

        while(len(num)<7):
            num = "0"+num
        
        return str(self.initials[0]+self.initials[1]+self.initials[2])+" "+str(num)
        

    def __eq__(self,other):
        return self.score == other.score

    def __lt__(self,other):
        return self.score < other.score

###Clase encargada de revisar los eventos del teclado
class keyboard():

    ##Se establecen las teclas a las que le prestaremos atencion
    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.SPACE = False
        self.SHIFT = False

    ##Revisa cuando se aprieta y cuando se suelta una tecla para recordar que teclas estan presionadas en que momento
    def check(self):
        keydowns = pygame.event.get(pygame.KEYDOWN)
        keyups = pygame.event.get(pygame.KEYUP)

        for keydown in keydowns:

            if keydown.key == K_ESCAPE:
                quitgame("now")
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
            elif keydown.key == K_LSHIFT:
                self.SHIFT = True
            elif keydown.key == K_DELETE:
                global GOD
                GOD = not GOD                
                global player
                if(GOD):
                    player.dmg = 10
                else:
                    player.dmg = 0.5
                    

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
            elif keyup.key == K_LSHIFT:
                self.SHIFT = False

#---------------------------------------------------

class blast(pygame.sprite.Sprite):
    
    def __init__(self,x,y,small = True):
        pygame.sprite.Sprite.__init__(self)
        self.blast = load_image("blast.png",IMG_DIR,True)        
        self.image = []
        self.size = 192
        self.speed = 0.2375
        self.counter = 0.0
        
        if(small):
            self.blast = pygame.transform.scale(self.blast,(96*5,96*4))
            self.size = 96
            self.speed = 0.38

        self.rect = Rect(x-self.size/2,y-self.size/2,self.size,self.size)

        for j in range(4):
            for i in range(5):
                self.image.append(self.blast.subsurface(Rect(i*self.size,j*self.size,self.size,self.size)))
        
    def animate(self):
        global screen
        screen.blit(self.image[int(self.counter)],self.rect)
        self.counter+=self.speed

        if(int(self.counter)>19):
            return True
        return False

        

# ------------------------------
# Funcion principal del juego
# ------------------------------


 
def main():
    #Se inicializa la libreria
    pygame.mixer.pre_init(44100, -16, 1, 4096) #Para minimizar el delay de sonido
    pygame.init()    

    global screen    
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.FULLSCREEN)
    pygame.display.set_caption("BulletHell")
    #Hermoso fondo de la batalla
    global fondo
    fondo = load_image("espeis.png",IMG_DIR,False)
    #GODMODE
    global GODSHIP
    GODSHIP = load_image("shipa.png",IMG_DIR,True)
    
    #Instanciamos al jugador y al jefe
    global player
    player = jugador()
    global boss
    boss = jefe()

    #?????????
    global clock
    clock = pygame.time.Clock()

    #Escondemos el mouse
    pygame.mouse.set_visible(False)

    #Establecemos los colores de los rectangulos que se dibujaran a mano (laser y barra de Hp del jefe)
    global colorbarra
    colorbarra = [Color(255,0,0,0),Color(220,0,0,0),Color(160,0,0,0),Color(100,0,0,0),Color(40,0,0,0)]
    global lasercolor
    lasercolor = [Color(0,0,255,0),Color(135,206,250,0),Color(255,255,255,0),Color(255,255,255,0)]
    global focuscolor
    focuscolor = [Color(0,0,0,0),Color(100,0,100,0),Color(221,160,221,0),Color(255,255,255,0)]

    #Creamos el teclado
    global key
    key = keyboard()




    
#-----------
# Epic Intro
#-----------

    #Score tester
    ##quitgame("")

    #Se carga y reproduce la musica para la epic intro... epicamente
    pygame.mixer.music.load(os.path.join(SONIDO_DIR,"space_0.mp3"))
    pygame.mixer.music.set_volume(1)
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
            quitgame()
            
        #Rendering
        screen.blit(fondo,(0,intro-360)) #Nos acercamos hacia el horizonte
        if(player.lazor):
            for l in range(4):
                if(player.focused):
                    screen.fill(focuscolor[l],player.laser[l])
                else:
                    screen.fill(lasercolor[l],player.laser[l])
        if GOD:
            screen.blit(GODSHIP,player.rect)
        else:
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
            intro += 5 #A que velocidad se scrollea la pantalla

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

        if not GOD:
            if(player.checkdmg(boss)):
                boss.balas = []
                quitgame("player")
        
        #Condiciones de fin
        if boss.hp <= 0:            
            quitgame("boss")
            
        #Posibles entradas del teclado y mouse
        key.check()

        #El player actua segun el input
        player.keyinput(key)
                    
        
        #Si se le indica al juego que ya no mas... ya no mas!
        if len(pygame.event.get(pygame.QUIT))>0:
            quitgame()

        #Rendering
        screen.blit(fondo,(0,0))
        if(player.lazor):
            for l in range(4):
                if(player.focused):
                    screen.fill(focuscolor[l],player.laser[l])
                else:
                    screen.fill(lasercolor[l],player.laser[l])        
        if GOD:
            screen.blit(GODSHIP,player.rect)
        else:
            screen.blit(player.image,player.rect)
        screen.blit(boss.image,boss.rect)   
        for b in boss.balas:
            screen.blit(b.image,(b.x-8,b.y-8))
        for m in boss.minions:
            screen.blit(m.image,(m.x-16,m.y-16))
        
        #UI
        for i in range(5):
            screen.fill(colorbarra[i],boss.hpbar[i])        
        
        pygame.display.flip()

#------------------------------------------------------


def quitgame(whodied=None):
    if(whodied != "now"):
        pygame.mixer.music.fadeout(1000)
        chanel = pygame.mixer.Channel(3)

        global player
        global clock
        global screen
        global fondo
        global boss
        global colorbarra
        global lasercolor
        global focuscolor
        global GODSHIP
        global key
        
        if(whodied == "player"):
            boom = load_sound("se_pldead00.wav",SONIDO_DIR)
            boom.set_volume(0.2)
            chanel.play(boom)
            bum = blast(player.rect.centerx,player.rect.centery)

            while(True):
                clock.tick(60)
                #Rendering
                screen.blit(fondo,(0,0))            

                screen.blit(boss.image,boss.rect)
                for b in boss.balas:
                    screen.blit(b.image,(b.x-8,b.y-8))
                for m in boss.minions:
                    screen.blit(m.image,(m.x-16,m.y-16))
                
                #UI
                for i in range(5):
                    screen.fill(colorbarra[i],boss.hpbar[i])
                if(bum.animate()):
                    break
                
                pygame.display.flip()
            
        elif(whodied == "boss"):
            player.score += 500000
            boom = load_sound("se_playerdead.wav",SONIDO_DIR)
            boom.set_volume(0.4)
            chanel.play(boom)

            bum = blast(boss.rect.centerx,boss.rect.centery,False)

            while(True):
                clock.tick(60)
                #Rendering

                # Posibles entradas del teclado y mouse
                key.check()

                # Dejamos al jugador moverse y disparar
                player.keyinput(key) 
                
                screen.blit(fondo,(0,0))
                if(player.lazor):
                    for l in range(4):
                        if(player.focused):
                            screen.fill(focuscolor[l],player.laser[l])
                        else:
                            screen.fill(lasercolor[l],player.laser[l])        
                if GOD:
                    screen.blit(GODSHIP,player.rect)
                else:
                    screen.blit(player.image,player.rect)
                    
                if(bum.animate()):
                    break
                
                pygame.display.flip()

            while(chanel.get_busy()):
                clock.tick(60)
                #Rendering

                # Posibles entradas del teclado y mouse
                key.check()

                # Dejamos al jugador moverse y disparar
                player.keyinput(key) 
                
                screen.blit(fondo,(0,0))
                if(player.lazor):
                    for l in range(4):
                        if(player.focused):
                            screen.fill(focuscolor[l],player.laser[l])
                        else:
                            screen.fill(lasercolor[l],player.laser[l])        
                if GOD:
                    screen.blit(GODSHIP,player.rect)
                else:
                    screen.blit(player.image,player.rect)

                pygame.display.flip()

        while(chanel.get_busy()):
            pass
#------------------------------------------------------------------
# HIGH SCORE
#------------------------------------------------------------------

        pygame.font.init()
        size = 30
        font = pygame.font.Font("./consola.ttf",size)
        
        #fail = open("./score.txt","r")
        scores = []
        #for f in fail:
        #    scores.append(score(f.replace("\n",""),False))
        #fail.close()
        
        #scores.append(score("--- "+str(player.score),True))

        #scores.sort()
        #scores.reverse()

        #Jurgen: Usamos HighscoreService aca
        global servicio
        if servicio != None:
            servicio.initialize()
            lis = servicio.getScores()
            for f in lis:
                scores.append(score(str(f[1])+" "+str(f[0]),False))
            while len(scores) < 10:
                scores.append(score("--- 0000000",False))
            scores.append(score("--- "+str(player.score),True))
            scores.sort()
            scores.reverse()

        high = False
        index = 10
        screen.fill(Color(0,0,0,0),Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(font.render("HIGH SCORES",True,Color(255,255,255,0),Color(0,0,0,0)),(SCREEN_WIDTH/2-len("HIGH SCORES")*size/2+70,60))
        for i in range(10):

            color = Color(255,255,255,0)

            print(len(scores))
            if(scores[i].isplayer):
                high = True
                index = i
                color = Color(0,155,200,0)

            screen.blit(font.render(str(scores[i]),True,color,Color(0,0,0,0)),(SCREEN_WIDTH/2-len(str(scores[i]))*size/2+70,100+size*i))
            #render(text, antialias, color, background=None)
            #pygame.freetype.Font.render_to(screen, (0,i*20),scores[i],Color(255,255,255,0),Color(0,0,0,255))
                
            #render_to(surf, dest, text, fgcolor=None, bgcolor=None, style=STYLE_DEFAULT, rotation=0, size=0) -> Rect

        pygame.display.flip()
        
#----------Name Input------------------
        if high:
            scores[index].initials = [" "," "," "]
            abcd = " "+string.ascii_uppercase+string.digits
            pointer = 0
            charter = 0
            enter = True
            change = load_sound("se_select00.wav",SONIDO_DIR)
            change.set_volume(0.1)
            ready = load_sound("se_cancel00.wav",SONIDO_DIR)
            ready.set_volume(0.1)
            
            while enter:
                clock.tick(60)
                screen.fill(Color(0,0,0,0),Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
                screen.blit(font.render("HIGH SCORES",True,Color(255,255,255,0),Color(0,0,0,0)),(SCREEN_WIDTH/2-len("HIGH SCORES")*size/2+70,60))
                for i in range(10):
                    color = Color(255,255,255,0)

                    if(scores[i].isplayer):
                        high = True
                        index = i
                        color = Color(0,155,200,0)

                    screen.blit(font.render(str(scores[i]),True,color,Color(0,0,0,0)),(SCREEN_WIDTH/2-len(str(scores[i]))*size/2+70,100+size*i))

                #Lectura teclado
                keydowns = pygame.event.get(pygame.KEYDOWN)
                
                for k in keydowns:
                    if k.key == K_RETURN or k.key == K_ESCAPE:
                        enter = False
                        ready.play(0)
                    elif k.key == K_UP:
                        pointer+=1
                        if(pointer == len(abcd)):
                            pointer = 0

                        change.play(0)

                        scores[index].initials[charter] = abcd[pointer]
                    elif k.key == K_DOWN:
                        pointer-=1
                        if(pointer == -1):
                            pointer = len(abcd)-1
                        change.play(0)
                        scores[index].initials[charter] = abcd[pointer]

                    elif k.key == K_LEFT:
                        charter -=1
                        if(charter == -1):
                            charter = 0

                        pointer = string.find(abcd,scores[index].initials[charter])

                        scores[index].initials[charter] = abcd[pointer]
                        change.play(0)

                    elif k.key == K_RIGHT or k.key == K_z:
                        charter+=1
                        if(charter == 3):
                            charter = 2
                            if(k.key == K_z):
                                enter = False
                                ready.play(0)
                            
                        pointer = string.find(abcd,scores[index].initials[charter])
                        scores[index].initials[charter] = abcd[pointer]
                        change.play(0)

                        
                        
                
                pygame.display.flip()
#-----------------------------------------------

        #Rendereamos la pantalla final
        screen.fill(Color(0,0,0,0),Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
        screen.blit(font.render("HIGH SCORES",True,Color(255,255,255,0),Color(0,0,0,0)),(SCREEN_WIDTH/2-len("HIGH SCORES")*size/2+70,60))        
        for i in range(10):
            screen.blit(font.render(str(scores[i]),True,Color(255,255,255,0),Color(0,0,0,0)),(SCREEN_WIDTH/2-len(str(scores[i]))*size/2+70,100+size*i))
        if not high:
            screen.blit(font.render("YOUR SCORE: "+str(scores[10].score),True,Color(0,155,200,0),Color(0,0,0,0)),(SCREEN_WIDTH/2-len(str(scores[10]))*size/2+20,100+size*11))
            
        pygame.display.flip()
        
        global EPIC
        while EPIC:
            keydowns = pygame.event.get(pygame.KEYDOWN)
            for k in keydowns:
                if k.key == K_RETURN or k.key == K_ESCAPE or k.key == K_z:
                    EPIC = False

        #fail = open("./score.txt","w")

        #for s in range(10):
        #    fail.write(str(scores[s])+"\n")

        #fail.close()
        #Jurgen: Usamos highscoreService
        for s in range(10):
            buf = str(scores[s]).split(" ")
            pts = buf[1]
            name = buf[0]
            servicio.register(pts,name)
        
    sys.exit(0)    

if __name__ == "__main__":
    main()
