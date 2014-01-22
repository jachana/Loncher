
global instance

import time

DEFAULT_USE_CONSOLE = True

class Logger:
	"""Clase que modela registro de log.
	"""

	def __init__(self, path, allowConsole = False, autoWriteback = True):
		self._path = path
		self._useConsole = allowConsole
		self._stamp = time.strftime("%d-%m-%y  %H%M")
		self._buf = ""
		self._writebackmode = autoWriteback

	def save(self):
		"""Metodo encargado de guardar el buffer de log en archivo.
		"""

		try:
			#Abrir archivo en modo append
			with open(self._path+self._stamp+".log",'a') as f:
				#Escribir lo que este en buffer de escritura
				f.write(self._buf)
				#vaciar buffer
				self._buf = ""
		except IOError:
			#Abrir archivo en modo write
			with open(self._path+self._stamp+".log",'w') as f:
				#Escribir lo que este en buffer de escritura
				f.write(self._buf)
				#vaciar buffer
				self._buf = ""


	def log(self,msg):
		"""Introduce una nueva entrada al log.
		"""

		#Agregamos mensaje a buffer
		self._buf = self._buf + time.strftime("%H:%M:%S")+" "+str(msg)+"\n"
		if self._useConsole is True:
			print(msg)
		if self._writebackmode is True:
			self.save()

def get_logger():
	"""Obtiene logger que ejecuta.
	"""

	global instance
	if instance is not None:
		instance = Logger("")
	return instance

def get_logger(path,allowConsole,autoWriteback):
	"""Obtiene el logger creado, y si no lo hay crea uno con los parametros dados.
	"""

	global instance
	if instance is not None:
		instance = Logger(path,allowConsole,autoWriteback)
	return instance

instance = Logger("./LON ")

if __name__ == "__main__":
	#test
	uut = get_logger("./test",True,True)
	for i in range(0,500):
		uut.log("Mensaje "+str(i))

