import os
import time

global instance

#Codigo desde http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})): pass

#Implementacion del logger
class Logger(Singleton):
	"""Clase que modela registro de log.
	"""

	def __init__(self, path, allowConsole = False, autoWriteback = True):
		#self._path = path
		self._useConsole = allowConsole
		self._stamp = time.strftime("%d-%m-%y  %H%M")
		self._buf = ""
		self._writebackmode = autoWriteback
		self._path = os.path.abspath(path+self._stamp+".log")

	def save(self):
		"""Metodo encargado de guardar el buffer de log en archivo.
		"""

		try:
			#Abrir archivo en modo append
			with open(self._path,'a') as f:
				#Escribir lo que este en buffer de escritura
				f.write(self._buf)
				#vaciar buffer
				self._buf = ""
		except IOError:
			#Abrir archivo en modo write
			with open(self._path,'w') as f:
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

	def disable_writeback(self):
		self._writebackmode = False

	def enable_writeback(self):
		self._writebackmode = True

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

instance = Logger("./logs/Launcher  ")

if __name__ == "__main__":
	#test
	uut = get_logger("./test",True,True)
	for i in range(0,500):
		uut.log("Mensaje "+str(i))

