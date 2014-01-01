import xml.etree.cElementTree as ET

#Modulo que se encarga de tener algunas configuraciones del launcher
servicePath = "./services"
gameDir = "./games"
gameList = "GameList_example.xml"

def Loadcfg():
	"""Metodo que carga la configuracion del launcher"""
	try:
		tree = ET.ElementTree(None,"ArcadeConfig.xml")
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
