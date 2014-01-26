#Instalador especifico de juegos

import zipfile
import system.game_man.gamelist as GL
import system.launcher_config as AC

def install(b_file,b_info):
	"""Instalador especifico de juegos.
	"""

	cfg = AC.loadcfg()
	games = GL.GameList(AC.gameList)

	#Ahora que tenemos la lista de juegos procedemos a instalar las cosas
	code = b_info.get_specific("code")
	#Verificamos que exista la carpeta, si no existe, la creamos
	import os
	t_path = "./games/"+code+"/"
	basedir = os.path.dirname(t_path)
	if not os.path.exists(basedir):
		os.makedirs(basedir)
	#Ahora que sabemos que existe, extraemos
	b_file.extractall(t_path)
	#Finalmente agregamos el juego a la lista
	games.add_game(t_path+b_info.get_specific("gameinfo"))
	games.save_xml(AC.gameList) #guardamos la lista actualizada
	#TODO: Modificar gameinfo.xml para asegurar paths
	return True