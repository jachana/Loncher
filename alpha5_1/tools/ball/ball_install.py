#modulo encargado de la instalacion de balls, delegando si es necesario

import zipfile
import tools.logger
import ball_info

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
		b_info = ball_info.BallInfo(b_file)
		if not check_dependencies(b_info):
			#Faltan requisitos
			log_.log("[BallInstall/install_ball] Missing requisites for ball "+path)
			#Informamos que no se realizo instalacion
			return False
		#Si pasa el check de dependencias, procedemos
		log_.log("[BallInstall/install_ball] Dependencies OK")
		#TODO: Llamar a instalador del tipo
		return_val = False
		try:
			imstr = "install."+str(b_info.get_balltype)
			eval("import imstr")
			return_val = eval("imstr.install(b,b_info)") #Solicitamos al instalador que haga la pega
		except Exception:
			#Algo salio mal, probablemente no existe el instalador de ese tipo
			log_.log("[BallInstall/install_ball] Exception during install, aborted. Is balltype standard or is the installHandler installed?")
			log_.log("Stack trace:")
			log_.log(str(Exception.args))
	#end_with
	return return_val

def check_dependencies(b_info):
	"""Funcion que dado un objeto BallInfo, verifica que se tengan los pre-requisitos instalados. Retorna True si estan presentes
	o False si no.
	"""

	return True

