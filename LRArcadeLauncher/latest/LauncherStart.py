#Script de inicio del Launcher
import tools
import GameList as GL
import servicesDiscovery as SD
import ArcadeConfig as AC
import ArcadeBackendFacade as ABF

def LauncherMain():
	#Comenzamos el inicio de las cosas
	#Cargamos la configuracion
	AC.Loadcfg()
	#Descubrimos servicios
	services = SD.discover(AC.servicePath)
    #Ejecutamos scripts de extensiones (si, codigo arbitrario)
	tools.runparts("./launcherinit.d/")
	#Obtenemos la lista de juegos
	lista = GL.GameList(AC.gameList)
	#Finalizamos con lanzar la interfaz
	#Primero inicializamos el backend
	fac = ABF.ArcadeBackendFacade(lista,services)
	#TODO: poner la GUI a andar

if __name__== "__main__":
	LauncherMain()
