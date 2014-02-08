#Instalador de balls genericos

import zipfile

def install(b_file,b_info):
	"""Instaldor de balls genericos.
	Simplemente extrae todo el contenido en la raiz del launcher.
	"""

	b_file.extractall(".")
	return True