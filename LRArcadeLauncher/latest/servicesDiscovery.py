#Script que se encarga de descubrir los servicios
import os
import imp

def discover(path):
        servlist = {}
        oldpath = os.getcwd()
        os.chdir(path)
        for files in os.listdir("."):
                if files.endswith(".py"):
                        loaded = imp.load_source("Loaded",files)
                        try:
                                name,serverFactory=eval("loaded.register()")
                                servlist[name]=serverFactory
                        except Exception:
                                pass
        os.chdir(oldpath)
        return servlist
								
if __name__ == "__main__":
        print( discover("./services/") )
