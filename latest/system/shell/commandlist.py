#script que permite conocer los comandos y ejecutarlos
import os
import imp

class CommandList:
	"""Clase que modela la lista de comandos.
	"""

	def __init__(self):
		self._clist = [] #No commands to begin with, we should have elements in the form (name,function pointer,docstring)

	def register(self):
		"""Registra los comandos.
		"""

		#copy/paste from service_discovery.. refactor?
		oldpath = os.getcwd() #avoiding trouble
		path = "./commands/"
        os.chdir(path)
        #look only in current dir
        for files in os.listdir("."):
                if files.endswith(".py"):
                        loaded = imp.load_source("commands."+os.path.splitext(os.path.basename(files))[0],files)
                        try:
                                #We attempt to find a register function in the script, note that a script might add more than one command
                                script_list = eval("loaded.register()")
                                #Now that we have the registrar list from the particular script, we add them to the main registry
                                self._clist += script_list
                        except Exception:
                                pass
        os.chdir(oldpath)
        #Now that registry process is complete, we sort the list so command searches can be faster
        self._clist.sort()

	def command(self, cmd):
		"""Interpreta un string como comando e intenta ejecutarlo.
		"""

		pass