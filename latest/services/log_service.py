#Servicio de Log
#Version 1.0 por Jurgen Heysen

import tools.logger

#Metodo que crea un objeto que representa el servicio a partir de
#un diccionario de argumentos y el codigo del juego
def factory(args,code):
	"""Crea un proveedor de servicio a partir de los argumentos para el juego indicado"""
	return LogServiceProvider(code)

#Metodo que registra el servicio al momento de descubrirlo
def register():
	"""Registra el servicio al descubrir servicios"""
	return "LogService",factory

class LogServiceProvider(object):
	"""Clase que provee acceso al log del Launcher"""
	def __init__(self, arg):
		super(LogServiceProvider, self).__init__()
		self._code = arg
		self._log = None
	
	def log(self,msg):
		"""Metodo que permite registrar el mensaje msg en el log.
		"""

		if self._log is None:
			self._log = tools.logger.get_logger("./"+self._code,False,True)
		self._log.log("["+self._code+"]"+str(msg))
	
