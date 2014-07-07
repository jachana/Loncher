import imp
import multiprocessing
import tools
import os
import sys
import abort_server

def launch_game(filename,classname,modulename,serviceinterface):
        """Lanza un juego en el proceso actual.
        """

        #tools.runparts(os.path.append(os.path.dirname(os.path.abspath(filename)),"\\gameinit.d"))#22-12-2013: Permitimos al juego agregar codigo arbitrario de inicializacion
        oldpath = os.getcwd() #Almacenamos el path viejo para no romper las cosas a la vuelta
        #ahora hacemos un cambio de directorio para no romper al juego
        os.chdir(os.path.dirname(os.path.abspath(filename)))
        #Ahora le damos partida al juego mediate un import, instancias y go
        onlyfile = os.path.basename(filename)
        #Ademas hacemos un append al path..
        sys.path.append(os.getcwd())
        log_ = tools.logger.Logger("./logs/Launcher ",True,True)
        #log_.disable_writeback()
        log_.log("[RL/lauch_game] "+onlyfile)
        #import dinaminco
        loaded = imp.load_source(modulename,onlyfile)
        #creamos el objeto
        toLoad = eval("loaded."+classname)()
        #partida
        toLoad.Go(serviceinterface)
        os.chdir(oldpath) #volvemos
        #log_.enable_writeback()

def launch_game_mt(filename,classname,modulename,serviceinterface):
        """Permite la carga de la clase classname en el archivo (path completo) filename con el nombre modulename (esto puede ser fijo)
        en un nuevo proceso
        """

        #Creamos un ovjeto proceso
        nproc = multiprocessing.Process(None,launch_game,"Juego",(filename,classname,modulename,serviceinterface),{})
        #Establecemos que es un sub-proceso prioritario
        nproc.daemon = False
        #Comenzamos su ejecucion
        nproc.start()
        #Entregamos handle de proceso a abort server
        srv = abort_server.abort_server(nproc)
        srv.gHandle = nproc
        #Esperamos que termine
        nproc.join()
        #Limpiamos handle del servidor
        srv.gHandle = None
        srv.kill()
