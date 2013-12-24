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
	return "HighScoreService",factory
	
class HighScoreServiceProvider:
	"""Servicio de punatjes para los juegos"""
	
	def __init__(self,code,max,storage):
		"""Code: Codigo del juego. max: numero de puntajes a guardar. storage: almacenamiento a utilizar"""
		self._code = code
		self._max = max
		self._storage = storage
		
	def register(self,score,name):
		"""Registra un score score para el jugador name, si esta en el top max"""
		pass
		
	def getScores(self):
		"""Retorna una lista con los scores guardados"""
		pass
