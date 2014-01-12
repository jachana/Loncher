#Servicio de Highscores

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
		import xml.etree.cElementTree as ET
		self._activated = True
		self._tree = ET.ElementTree()
		self._root = self._tree.getroot()
		try:
			self._tree = ET.ElementTree(None,"./data/scores/"+self._code+".xml")
			self._root = self._tree.getroot()
			for score in self._root.findall("score"):
				self._scorelist.append( (score.get("points"),score.get("name")) )
			self._scorelist = self._scorelist.sort()
			if len(self._scorelist) > max:
				self._scorelist = self._scorelist[max:]
		except Exception:
			pass
		
	def register(self,score,name):
		"""Registra un score score para el jugador name, si esta en el top max"""
		if not self._activated:
			return
		self._scorelist.append( (score,name) )
		nuevo = ET.SubElement(self._root,"score")
		nuevo.set("points",score)
		nuevo.set("name",name)
		self._tree.write("./data/scores/"+self._code+".xml")
		
	def getScores(self):
		"""Retorna una lista con los scores guardados"""
		return self._scorelist
