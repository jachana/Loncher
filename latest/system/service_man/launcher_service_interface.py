#modulo que se enncargara de entregar servicios solicitados al juego.
import tools.logger

class LauncherServiceInterface:
	"""Clase interface que expone servicios solicitados"""

	def __init__(self,code,gameservicedic,systemservicedic):
		self._services = {}
		self._log = tools.logger.Logger("./logs/Launcher ",True,True)
		#Inicializamos los servicios que se pidan con lo que encontremos
		for serv in gameservicedic.keys():
			try:
				#intentamos inicializar el sevicio con la data, pero podria faltar data o no estar el servicio
				self._services[serv] = systemservicedic[serv](gameservicedic[serv],code)
			except Exception:
				self._log.log("[LSI/init] [CRITICAL] Service "+str(serv)+" not found for "+str(code))

	def get_services(self):
		"""Entrega un diccionario con los servicios disponibles"""
		#Entrega el dict sin miramientos
		return self._services

	def get_service(self,name):
		"""Intenta obtener el proveedor del servicio name, entrega None si no se encuentra disponible"""
		#forma segura de obtener un servicio
		try:
			return self._services[name]
		except Exception:
			return None
