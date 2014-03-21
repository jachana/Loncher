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
		path = "./system/shell/commands/"
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

    def _bsearch(self, name, init_index, end_index):
    	"""Performs a binary-search over the command list looking for the processor. returns a handle to the processor if found or None otherwise.
    	"""

    	#Base case: lenght is 1 or 0
    	if init_index - end_index < 0:
    		if self._clist[init_index][0] == name:
    			return self._clist[init_index]
    		else:
    			return None
    	#Base case: element at middle point
    	if self._clist[middle][0] == name:
    		return self._clist[middle]
    	#Not in base case, recursive call
    	middle = int((init_index + end_index)/2)
    	if self._clist[middle][0] < name:
    		#We need the right side list
    		return self._bsearch(name,middle,end_index)
    	if self._clist[middle][0] > name:
    		#left side
    		return self._bsearch(name,init_index,middle)

	def command(self, cmd):
		"""Interpreta un string como comando e intenta ejecutarlo.
		"""

		scmd = str(cmd) #First, we meke sure we are dealing with strings
		l_scmd = scmd.split(" ") #We make a split on whitespaces
		args = "" #We reserve a buffer for arguments, we start by assuming it is empty
		#Now we concatenate args (if any)
		if len(l_scmd) > 1:
			for i in range(1,len(l_scmd)+1):
				args = args + l_scmd[i] + " "
		#Now we have the args, and the command. We isolate it for code clarance purposes.
		mcmd = l_scmd[0]
		mcmd = mcmd.lower() #commands should be lowercase
		#Now, we perform a binary-search over the command list
		cproc = self._bsearch(mcmd,0,len(self._clist)) #We allocate a variable for referencing the command-processor
		#Now, we execute
		if cproc is not None:
			cproc[1](args)
		else:
			pass #TODO: something here
