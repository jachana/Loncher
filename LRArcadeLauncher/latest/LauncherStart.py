#Script de inicio del Launcher
import tools
import GameList as GL
def LauncherMain():
	#Comenzamos el inicio de las cosas
        #Ejecutamos scripts de extensiones (si, codigo arbitrario)
	tools.runparts("./launcherinit.d/")
	#Obtenemos la lista de juegos
	lista = GL.GameList('GameList_example.xml')
	#Finalizamos con lanzar la interfaz
	#TODO: Lanzar interfaz

if __name__== "__main__":
	LauncherMain()
