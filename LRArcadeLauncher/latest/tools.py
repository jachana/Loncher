import os
import imp
#La idea es acá tener métodos de ayuda
def runparts(path):
	"""Método que dado una carpeta, ejecuta todo lo que haya en ella, siempre que tenga el método exec"""
	os.chdir(path)
	for files in os.listdir("."):
    if files.endswith(".py"):
        loaded = imp.load_source("Loaded",files)
		try:
			eval("loaded.exec()")
		except Exception:
			pass
