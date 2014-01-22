import xml.etree.cElementTree as ET

#Modulo que se encarga de tener algunas configuraciones del launcher
global servicePath 
servicePath= "./services"
global gameDir 
gameDir= "./games"
global gameList 
gameList= "GameList_example.xml"

def Loadcfg():
	"""Metodo que carga la configuracion del launcher"""
	global servicePath
	global gameDir
	global gameList
	try:
		tree = ET.ElementTree(None,".\Config\ArcadeConfig.xml")
		root = tree.getroot()
		#cargamos los parametros
		for n in root.findall("servicePath"):
			servicePath = n.get("dir")
		for n in root.findall("gameDir"):
			gameDir = n.get("dir")
		for n in root.findall("gameList"):
			gameList = n.get("src")
	except Exception:
		print("[WARN] No config file found, using default")
