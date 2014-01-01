import imp
import StartBase
import multiprocessing
import tools
import os

def LaunchGameFromFile(filename,classname,modulename,serviceinterface):
        """Usar metodo MT mejor."""
        #tools.runparts(os.path.append(os.path.dirname(os.path.abspath(filename)),"\\gameinit.d"))#22-12-2013: Permitimos al juego agregar codigo arbitrario de inicializacion
        loaded = imp.load_source(modulename,filename)
        toLoad = eval("loaded."+classname)()
        toLoad.Go(serviceinterface)

def LaunchGameFromFileMT(filename,classname,modulename,serviceinterface):
        """Permite la carga de la clase classname en el archivo (path completo) filename con el nombre modulename (esto puede ser fijo)"""
        nproc = multiprocessing.Process(None,LaunchGameFromFile,"Juego",(filename,classname,modulename,serviceinterface),{})
        nproc.daemon = False
        nproc.start()
        nproc.join()
