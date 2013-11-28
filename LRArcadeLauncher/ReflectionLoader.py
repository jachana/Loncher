from LRArcadeLauncher import GameCaller
import imp
import StartBase
import multiprocessing

def LaunchGameFromFile(filename,classname,modulename):
        loaded = imp.load_source(modulename,filename)
        toLoad = eval("loaded."+classname)()
        caller = GameCaller()
        #caller.GameCall(toLoad,True)
        toLoad.Go()
        #Here be test
        #GameThead = multiprocessing.Process(None,toLoad.Go,"Juego",(),{})
        #GameThead.daemon = False #Nos aseguramos que Phyton no puede cerrar si el juego no ha cerrado
        #GameThead.start()
        #GameThead.join()
        #Here be end test

def LaunchGameFromFileMT(filename,classname,modulename):
        nproc = multiprocessing.Process(None,LaunchGameFromFile,"Juego",(filename,classname,modulename),{})
        nproc.daemon = False
        nproc.start()
        nproc.join()
