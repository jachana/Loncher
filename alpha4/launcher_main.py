#Script de inicio del Launcher
import system.tools as tools
import system.game_man.gamelist as GL
import system.service_man.service_discovery as SD
import system.launcher_config as AC
import system.backend_facade as ABF
import ui.ArcadeCLI as ArcadeCLI
import argparse
import ui.Interfaz as Interfaz
import tools.logger as logger

parser = argparse.ArgumentParser()
parser.add_argument("-c","--console", action="store_true", help="Uses CLI instead of GUI")
args = parser.parse_args()

def LauncherMain():
	#Comenzamos el inicio de las cosas
	#Cargamos la configuracion
	AC.Loadcfg()
	#Inicializamos el logger
	log = logger.get_logger("./logs/Launcher ",True,True)
	#Descubrimos servicios
	services = SD.discover(AC.servicePath)
    #Ejecutamos scripts de extensiones (si, codigo arbitrario)
	tools.runparts("./launcherinit.d/")
	#Obtenemos la lista de juegos
	lista = GL.GameList(AC.gameList)
	log.log(str(lista)) #debug
	#Finalizamos con lanzar la interfaz
	#Primero inicializamos el backend
	fac = ABF.ArcadeBackendFacade(lista,services)
	#TODO: poner la GUI a andar
	gui = None
	if args.console:
		gui = ArcadeCLI.ArcadeCLI(fac)
	else:
		gui = Interfaz.ArcadeGUI(fac)
	gui.go()

if __name__== "__main__":
	LauncherMain()
