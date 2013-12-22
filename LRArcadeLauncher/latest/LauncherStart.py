#Script de inicio del Launcher
import tools
def LauncherMain():
	#Comenzamos el inicio de las cosas
	#Primero obtenemos la lista de juegos
	#TODO: Obtener lista
	#Ahora ejecutamos scripts de extensiones (si, código arbitrario)
	tools.runparts("./launcherinit.d/")
	#Finalizamos con lanzar la interfaz
	#TODO: Lanzar interfaz

if __name__== "__main__":
	LauncherMain()
