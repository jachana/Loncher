import game_man.reflection_loader as RL
import game_man.gamelist as GameList
import game_man.gameinfo
import service_man.launcher_service_interface as LSI
import tools
import os
#Esto hace el link logico con el resto del backend del Launcher, asi la UI puede ser mas tonta

class ArcadeBackendFacade:
	def __init__(self,gl,services):
		#gl lista de juegos, services lista de servicios
		self._games = gl
		self._services = services
		self._log = tools.logger.Logger("./logs/Launcher ",True,True)

	def load_game(self,code):
		"""Dado un juego seleccionado, solicita su entrada en ejecucion"""
		game = None
		gameServiceList = None
		#buscamos el codigo en la lista (se supone unico)
		for g in self._games.get_list():
			self._log.log("[BF/load_game] Analisis "+code+" = "+g.getCode())
			if code == g.getCode():
				self._log.log("[BF/load_game]Lucky")
				#si lo encontramos guardamos la referencia
				game = g
				gameServiceList = g.get_services()
		if g == None:
			self._log.log("[CRITICAL] Attempted to launch"+code+" but wasn't on GameList")
			return #interrumpimos el lanzamiento
		#Creamos la interfaz de servicios para el juego
		interface = LSI.LauncherServiceInterface(code,gameServiceList,self._services)
		#Ahora que tenemos la info, procedemos al lanzamiento
		self._log.log("[BF/load_game] Path: "+str(os.getcwd()))
		RL.launch_game_mt(game.getPath(),game.getClassName(),code,interface)

	def get_gamelist(self):
		#Esta lista la obtenemos en init de launcher, pero la GUI la puede necesitar antes
		return self._games
