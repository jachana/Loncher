#Servicio de Highscores
#Version 1.0 por Jurgen Heysen

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import ArcadeConfig as AC

#Metodo que crea un objeto que representa el servicio a partir de
#un diccionario de argumentos y el codigo del juego
def factory(args,code):
	"""Crea un proveedor de servicio a partir de los argumentos para el juego indicado"""
	max = args["max"]
	storage = args["storage"]
	return HighScoreServiceProvider(code,max,storage)

#Metodo que registra el servicio al momento de descubrirlo
def register():
	"""Registra el servicio al descubrir servicios"""
	return "HighscoreService",factory
	
class HighScoreServiceProvider:
	"""Servicio de punatjes para los juegos"""
	
	def __init__(self,code,max,storage):
		"""Code: Codigo del juego. max: numero de puntajes a guardar. storage: almacenamiento a utilizar"""
		self._code = code
		self._max = max
		self._storage = storage
		self._tree = None
		self._root = None
		self._activated = False
		self._scorelist = []
		self._path=currentdir+"./data/scores/"+str(self._code)+".xml"
		

	def initialize(self):
		"""Inicializa el proveedor"""
		import xml.etree.cElementTree as ET
		self._activated = True
		self._tree = ET.ElementTree()
		self._root = self._tree.getroot()
		self._scorelist = []
		try:
			self._tree = ET.ElementTree(None,self._path)
			self._root = self._tree.getroot()
			for score in self._root.findall("Score"):
				self._scorelist.append( (score.get("points"),score.get("name")) )
			self._scorelist.sort()
			if len(self._scorelist) > max:
                                nuescores = []
				for i in range(0,max):
                                        nuescores.append(self._scorelist[i])
                                self._scorelist = nuescores
		except Exception as e:
			import os
			basedir = os.path.dirname(self._path)
			if not os.path.exists(basedir):
				os.makedirs(basedir)
			open(self._path, 'a').close()
			self._root = ET.Element("Scores")
			self._tree = ET.ElementTree(self._root)
			self._tree.write(self._path)
			if self._scorelist == None:
                                self._scorelist = []
		
	def register(self,score,name):
		"""Registra un score score para el jugador name, si esta en el top max"""
		import xml.etree.cElementTree as ET
		if not self._activated:
			return
		self._scorelist.append( (score,name) )
		nuevo = ET.SubElement(self._root,"Score")
		nuevo.set("points",str(score))
		nuevo.set("name",name)
		self._tree.write(self._path)
		
	def getScores(self):
		"""Retorna una lista con los scores guardados"""
		return self._scorelist
