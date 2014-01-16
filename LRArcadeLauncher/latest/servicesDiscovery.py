#Script que se encarga de descubrir los servicios
import os
import imp

def discover(path):
        servlist = {}
        oldpath = os.getcwd() #evitamos problemas
        os.chdir(path)
        #Buscamos todos los archivos en la carpeta de busqueda
        for files in os.listdir("."):
                #Pero sources de python
                if files.endswith(".py"):
                        #import dinamico
                        loaded = imp.load_source("services."+os.path.splitext(os.path.basename(files))[0],files)
                        try:
                                #podria no ser un servicio, sino un test case por ejemplo
                                name,serverFactory=eval("loaded.register()")
                                #Si no se cae, lo anadimos al dict
                                servlist[name]=serverFactory
                        except Exception:
                                pass
        os.chdir(oldpath) #volvemos a la carpeta anterior
        return servlist
								
if __name__ == "__main__":
        print( discover("./services/") )
