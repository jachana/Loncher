#Servicio de Highscores
#Version 1.0 por Jurgen Heysen

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
		

	def initialize(self):
		"""Inicializa el proveedor"""
		import xml.etree.cElementTree as ET
		self._activated = True
		self._tree = ET.ElementTree()
		self._root = self._tree.getroot()
		self._scorelist = []
		try:
			print("Init main block begin")
			self._tree = ET.ElementTree(None,"./data/scores/"+str(self._code)+".xml")
			self._root = self._tree.getroot()
			for score in self._root.findall("Score"):
				self._scorelist.append( (score.get("points"),score.get("name")) )
                        print("Pre-sort: "+str(self._scorelist))
			self._scorelist.sort()
			print("sorted list, list: "+str(self._scorelist))
			if len(self._scorelist) > max:
				nuescores = []
				for i in range(0,max):
                                        nuescores.append(self._scorelist[i])
                                self._scorelist = nuescores
			print("Init main block end")
		except Exception as e:
			print("Init Exception block")
			import os
			basedir = os.path.dirname("./data/scores/"+str(self._code)+".xml")
			if not os.path.exists(basedir):
				os.makedirs(basedir)
			open("./data/scores/"+str(self._code)+".xml", 'a').close()
			self._root = ET.Element("Scores")
			self._tree = ET.ElementTree(self._root)
			self._tree.write("./data/scores/"+str(self._code)+".xml")
			if self._scorelist == None:
                                self._scorelist = []
			print("Init exception block end")
			print("Exception args:")
			print(str(e.args))
		
	def register(self,score,name):
		"""Registra un score score para el jugador name, si esta en el top max"""
		import xml.etree.cElementTree as ET
		if not self._activated:
			return
		self._scorelist.append( (score,name) )
		nuevo = ET.SubElement(self._root,"Score")
		nuevo.set("points",str(score))
		nuevo.set("name",name)
		self._tree.write("./data/scores/"+str(self._code)+".xml")
		
	def getScores(self):
		"""Retorna una lista con los scores guardados"""
		return self._scorelist
