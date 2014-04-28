from Tkinter import *
import system.game_man.gamelist as GL
import system.game_man.gameinfo as GI
import system.backend_facade as ABF
from PIL import ImageTk, Image
import tools
import random
import math
import pygame.joystick
import pygame.event
import pygame

#Constants

STR_NODESC = "No description Available" #No description string
STR_WINTITLE = "Arcade Launcher 1.0.0" #Window Title

W_MINWIDTH = 1024
W_MINHEIGHT = 768

FL_BG = "./ui/res/bg.png" #Backgrund image location
FL_NOSS = "./ui/res/noss.png" #No Screenshot Available Image

class ArcadeGUIEx:
	"""Graphic User Interface for Arcade
	"""

	def __init__(self,back):
		"""Constructor for GUI object, requieres a backend instance to be passed as argument.
		"""
		
		#Internal variable definitions
		self._log = tools.logger.Logger("./logs/Launcher ",True,True) #Logger handle
		self._log.log("[GUI/init] Init: Variable definition")
		self._back = back #backend handle
		self._winroot = Tk() #Main window handle
		self._gamedict = {} #Dictionary for keeping track of the games

		#Window Definiton
		self._log.log("[GUI/Init] Init: Window Definition")
		self._winroot.title(STR_WINTITLE)
		self._winroot.minsize(W_MINWIDTH,W_MINHEIGHT)
		self._winroot.overrideredirect(True)
		self._winroot.geometry("{0}x{1}+0+0".format(self._winroot.winfo_screenwidth(), self._winroot.winfo_screenheight()))
		#TODO: Window name, size, etc.

		#Background
		self._log.log("[GUI/Init] Setting up background")
		self._bgfile = Image.open(FL_BG) #background image reference
		self._background = ImageTk.PhotoImage(self._bgfile) #background image usable reference
		
                widthratio = math.ceil(self._winroot.winfo_screenwidth() / self._bgfile.size[0])+1 #Screen/Image Width ratio, needed for tessellation.
                heightratio = math.ceil(self._winroot.winfo_screenheight() / self._bgfile.size[1])+1 #Screen/Image Height ratio, needed for tessellation.

                self._bg = [] #Background labels
                for s in range (int(widthratio*heightratio)):
                        self._bg.append(Label(self._winroot, image = self._background, borderwidth = 0)) 
                
                for j in range(int(heightratio)):
                        for i in range(int(widthratio)):
                                #Tessellation
                                self._bg[int(i+j*widthratio)].place(x=i*(self._bgfile.size[0]),y=j*(self._bgfile.size[1]),anchor = NW) #Draw each piece of the background

		#Gamelist
		self._log.log("[GUI/Init] Setting up gamelist")
		#scrollbar = Scrollbar(self._winroot, orient=VERTICAL) #So we can see if there is more
		self._gl = Listbox(self._winroot) #Widget
		#scrollbar.config(command=self._gl.yview)
		#scrollbar.pack(side=RIGHT, fill=Y)
		self._gl.pack() #Draw it
		self._gl.bind("<<ListboxSelect>>",self.on_list_select) #selection update method binding
		self._gl.bind("<Return>",self.on_list_return) #selection method binding
		self._log.log("[GUI/Init] Beggining GameList scanning")
		for game in self._back.get_gamelist().get_list():
			#We first add the title to the list if it's not loaded before
			if not game.getGameName() in self._gamedict:
				self._gl.insert(END,game.getGameName())
				self._log.log("[GUI/Init] Added "+game.getGameName()+" to the list.")
			#Now we update the gameinfo reference so we can keep track of it
			self._gamedict[game.getGameName()] = game
			self._log.log("[GUI/Init] Registered "+game.getGameName()+" as "+game.getCode())
		#Population process ended, report
		self._log.log("[GUI/Init] Gamelist population process ended.")
		#Set item as active
		self._gl.selection_set(0)
		self._gl.activate(0)
		self._gl.focus_set()
		self._gl.config(height = '27')
		self._gl.grid(row=0, column=1) #draw list

		#Screenshot Area
		self._log.log("[GUI/Init] Setting up screenshot area")
		self._sswidget = Label(self._winroot)
		self._sswidget.grid(row = 0, column = 3)

		#Game Description
		self._log.log("[GUI/Init] Setting up description zone")
		self._gamedescrp = Label(self._winroot, text = STR_NODESC) #WWidget
		self._gamedescrp.grid(row = 2, column = 2, columnspan = 3, sticky = W+E+N+S, padx = 5, pady = 5,rowspan = 5) #Draw it, note, we'll update it's text

		#Now we have finished makig the screen, so we'll report and force update the info
		self._log.log("[GUI/Init] Init process finished.")
		self.on_list_select(None) #Force update

		#Joystick support section
		self._log.log("[GUI/Init] Initiating Joystick compatibility module")
		self.joystickOk = False

		##Gotten from http://forums.majorgeeks.com/showthread.php?t=254317
		#Initialize joystick module
		pygame.joystick.init()
		pygame.init()
		# Allow multiple joysticks
		self.joy = []
		# Declare axis displacement vector for an Xbox 360 Controller
		self.displacement = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		# Look for a connected joystick
		if pygame.joystick.get_count() > 0:
			self._log.log("[GUI/Init] "+str(pygame.joystick.get_count())+" Joysticks found")
			self.joystickOk = True
			numJoys = pygame.joystick.get_count()
			for i in range(numJoys):
				myJoy = pygame.joystick.Joystick(i)
				myJoy.init()
				self.joy.append(myJoy)
				self._log.log("[GUI/Init] Joytick"+str(i)+": "+self.joy[i].get_name())
		else:
			self._log.log("[GUI/Init] No Joystick detected")
		self._log.log("[GUI/Init] Joystick Initialization ended with result "+str(self.joystickOk))
		#Finally, we register for polling
		self._winroot.after(100,self.on_joy_tick)

	def go(self):
		"""Requiered method for init script.
		"""

		self._winroot.mainloop()

	def on_list_select(self, evt):
		"""Handles Selection change event on gamelist, to update game info displayed.
		"""

		#We'll take advantage of keeping track of the game Titles so we can speed up this process
		name = self._gl.get(ACTIVE)
		#First, we update the description
		self._gamedescrp.configure(text = self._gamedict[name].getDescripcion())
		#Reporting
		self._log.log("[GUI/list_select] Selected game "+name)
		#Update Screenshots
		sslist = self._gamedict[name].getScreenshots()
		ssimag = None
		if len(sslist) > 0:
			num = random.randint(0,len(sslist)-1)
			self._log.log("[GUI/list_select] Using screenshot "+sslist[num]+" out of "+str(len(sslist))+" Available.")
			ssimag = Image.open(sslist[num])
		else:
			self._log.log("[GUI/list_select] No screenshots found for display")
			ssimag = Image.open(FL_NOSS)
		#Now that we have file handler, we create a ImageTk and draw
		ss = ImageTk.PhotoImage(ssimag)
		self._sswidget.configure(image = ss)
		self._sswidget.image = ss

	def on_list_return(self, evt):
		"""Handles return key hit on gamelist to load a game.
		"""

		#We report the action and see what happens.
		#First, we get the gamecode
		code = self._gamedict[self._gl.get(ACTIVE)].getCode()
		if code is None:
			self._log.log("[GUI/list_return] Attempted to launch game with no code")
			pass
		else:
			self._log.log("[GUI/list_return] Launching game "+self._gl.get(ACTIVE)+" as "+code)
			self._back.load_game(code)

	def on_joy_tick(self):
		"""Processes joytick information to update selection.
		"""

		#We ask the pygame event pump for events
		for event in pygame.event.get():
			if event.type == pygame.JOYBUTTONDOWN:
				self._log.log("[GUI/joy_tick] Joystick button pressed.")
				self.on_list_return(None) #Launch selected
			if event.type == pygame.JOYBUTTONUP:
				self._log.log("[GUI/joy_tick] Joystick button released.")
			if event.type == pygame.JOYHATMOTION:
				val = event.value
				xval = val[0]
				yval = val[1]
				self._log.log("[GUI/joy_tick] Joystick Hat moved with x="+str(xval)+"and y="+str(yval))
				self.joy_select(xval)
				self.joy_select(yval)
			if event.type == pygame.JOYAXISMOTION:
				val = event.value
				self._log.log("[GUI/joy_tick] Joystick axis moved with value "+str(val))
				self.joy_select(val)
		#we ask tkinter to re-schedule the event
		self._winroot.after(100,self.on_joy_tick)

	def joy_select(self,value):
		"""Makes the selection on the Listbox
		"""

		if value > 0.5:
			self._log.log("[GUI/joy_select] Selecting up")
		if value < -0.5:
			self._log.log("[GUI/joy_select] Selecting down")
