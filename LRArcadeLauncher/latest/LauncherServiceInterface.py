#modulo que se enncargara de entregar servicios solicitados al juego.

class LauncherServiceInterface:
	"""Clase interface que expone servicios solicitados"""

	def __init__(self,code,gameservicedic,systemservicedic):
		self._services = {}
		#Inicializamos los servicios que se pidan con lo que encontremos
		for serv in gameservicedic.keys():
			try:
				self._services[serv] = systemservicedic[serv](gameservicedic[serv],code)
			except Exception:
				print("[CRITICAL] Service "+str(serv)+" not found for "+str(code))

	def getServices(self):
		return self._services

	def getService(self,name):
		try:
			return self._services[name]
		except Exception:
			return None