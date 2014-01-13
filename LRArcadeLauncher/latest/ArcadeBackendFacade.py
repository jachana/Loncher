import ReflectionLoader as RL
import GameList
import GameInfo
import LauncherServiceInterface as LSI
import os
#Esto hace el link logico con el resto del backend del Launcher, asi la UI puede ser mas tonta

class ArcadeBackendFacade:
	def __init__(self,gl,services):
		self._games = gl
		self._services = services

	def LoadGame(self,code):
		"""Dado un juego seleccionado, solicita su entrada en ejecucion"""
		game = None
		gameServiceList = None
		for g in self._games.getList():
			print("Analisis "+code+" = "+g.getCode())
			if code == g.getCode():
				print("Lucky")
				game = g
				gameServiceList = g.getServices()
		if g == None:
			print("[CRITICAL] Attempted to launch"+code+" but wasn't on GameList")
			return #interrumpimos el lanzamiento
		interface = LSI.LauncherServiceInterface(code,gameServiceList,self._services)
		#Ahora que tenemos la info, procedemos al lanzamiento
		print("Path: "+str(os.getcwd()))
		RL.LaunchGameFromFileMT(game.getPath(),game.getClassName(),code,interface)

	def getGameList(self):
		return self._games
