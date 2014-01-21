import os
import imp
#La idea es aca tener metodos de ayuda
def runparts(path):
        """Metodo que dado una carpeta, ejecuta todo lo que haya en ella, siempre que tenga el metodo exec"""
        oldpath = os.getcwd()
        os.chdir(path)
        for files in os.listdir("."):
                if files.endswith(".py"):
                        loaded = imp.load_source("Loaded",files)
                        try:
                                eval("loaded.exec()")
                        except Exception:
                                pass
        os.chdir(oldpath)
