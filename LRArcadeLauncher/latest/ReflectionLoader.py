import imp
import StartBase
import multiprocessing
import tools
import os
import sys

def LaunchGameFromFile(filename,classname,modulename,serviceinterface):
        """Usar metodo MT mejor."""
        #tools.runparts(os.path.append(os.path.dirname(os.path.abspath(filename)),"\\gameinit.d"))#22-12-2013: Permitimos al juego agregar codigo arbitrario de inicializacion
        oldpath = os.getcwd() #Almacenamos el path viejo para no romper las cosas a la vuelta
        #ahora hacemos un cambio de directorio para no romper al juego
        os.chdir(os.path.dirname(os.path.abspath(filename)))
        #Ahora le damos partida al juego mediate un import, instancias y go
        onlyfile = os.path.basename(filename)
        #Ademas hacemos un append al path..
        sys.path.append(os.getcwd())
        print(onlyfile)
        #import dinaminco
        loaded = imp.load_source(modulename,onlyfile)
        #creamos el objeto
        toLoad = eval("loaded."+classname)()
        #partida
        toLoad.Go(serviceinterface)
        os.chdir(oldpath) #volvemos

def LaunchGameFromFileMT(filename,classname,modulename,serviceinterface):
        """Permite la carga de la clase classname en el archivo (path completo) filename con el nombre modulename (esto puede ser fijo)"""
        nproc = multiprocessing.Process(None,LaunchGameFromFile,"Juego",(filename,classname,modulename,serviceinterface),{})
        nproc.daemon = False
        nproc.start()
        nproc.join()
