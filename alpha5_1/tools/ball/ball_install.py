#modulo encargado de la instalacion de balls, delegando si es necesario

import zipfile
import tools.logger

global log_
log_ = logger.get_logger()

def install_ball(path):
	"""Funcion que permite instalar un ball, dado el path a este.
	"""

	#El primer paso es abrir el archivo
	log_.log("[BallInstall/install_ball] Opening "+path)
	with zipfile.ZipFile(path,"r") as b:
		b_file = b.open("BallInfo.xml")
		#Ahora se verifican que existan las dependencias
		if not check_dependencies(b_file):
			#Faltan requisitos
			log_.log("[BallInstall/install_ball] Missing requisites for ball "+path)
		#Si pasa el check de dependencias, procedemos
		log_.log("[BallInstall/install_ball] Dependencies OK")
		#TODO: Llamar a instalador del tipo
	#end_with

def check_dependencies(b_info):
	"""Funcion que dado un objeto BallInfo, verifica que se tengan los pre-requisitos instalados. Retorna True si estan presentes
	o False si no.
	"""

	pass

