#Script que se encarga de borrar los .pyc para hacer un release
import os
import imp

def discover(path):
        oldpath = os.getcwd() #evitamos problemas
        os.chdir(path)
        #Buscamos todos los archivos en la carpeta de busqueda
        for files in os.listdir("."):
                #Pero sources de python
                if files.endswith(".pyc"):
                        print("Deleting "+str(files))
                        os.remove(files)
                if os.path.isdir(files):
                        print("entering "+str(files))
                        discover(files)
        os.chdir(oldpath) #volvemos a la carpeta anterior
								
if __name__ == "__main__":
        print( discover("..") )