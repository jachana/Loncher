#Clase que modela la informacion que expone un juego, se carga desde un GameInfo.xml
import xml.etree.cElementTree as ET
import os

class GameInfo:
	def __init__(self,XmlPath):
		"""Crea un objeto que represneta la info de un juego"""
		self._tree = ET.ElementTree() #Base del arbol
		self._gamename = "Juego" #Nombre del juego
		self._gamecode = "G0" #codigo unico
		self._version = 001 #version
		self._builddate = "01-01-2014" #fecha de build
		self._description = "Descripcion" #Descripcion a mostrar
		self._path = "./StartBase.py" #Path del script a correr
		self._classname = "Start" #Nombre de la clase quye contiene a go
		self._authors = [] #lista de autores
		self._services = {} #Diccionario de servicios con sus parametros
		self._adddata = [] #datos adicionales y misteriosos
		self._screenshots = [] #paths de ss
		#Si no estamos haciendo un objeto generico, cargamos data
		if XmlPath != '':
			self.loadXml(XmlPath)
		
	def __str__(self):
		#Asi imprimo la lista de juegos en la CLI y en game_install tralala
		return str(self._gamecode)+" : "+str(self._gamename)+" v"+str(self._version)+" ("+str(self._builddate)+") on "+str(self._path)+":"+str(self._classname)
		
	def loadXml(self,XmlPath):
		"""Carga la informacion desde un archivo"""
		#Cragar datos desde el Xml
		self._tree = ET.ElementTree(None,XmlPath)
		root = self._tree.getroot()
		#Leemos datos basicos desde el Xml
		#Prima el ultimo nodo si hay mas de uno
		for name in root.findall('Title'):
			self._gamename = name.text
		for code in root.findall('Code'):
			self._gamecode = code.text
		for ver in root.findall('Version'):	
			self._version = ver.text
		for des in root.findall('Description'):
			self._description = des.text
		for cl in root.findall('MainClass'):
			self._classname = cl.get('name')
			self._path = cl.get('file')
		for dat in root.findall('Date'):
			self._builddate = dat.text
		#Cargamos las rutas de las screenshots
		for ss_sec in root.findall('Screenshots'):
			for ss in ss_sec.findall('Screenshot'):
				self._screenshots.append(ss.get('src'))
		#Ahora cargamos la informacion de los servicios (Critico)
		for services in root.findall('Services'):
			for service in services.findall('Service'):
				#self._services.append( (service.get('name'),service.attrib) )
                                self._services[service.get("name")]=service.attrib
		#Finalmente cargamos los autores y la data adicional
		for authors in root.findall('Authors'):
			for author in authors.findall('Author'):
				self._authors.append(author.get('name'))
		for adddata in root.findall('AdditionalData'):
			for data in adddata:
				self._adddata.append( (data.tag,data.attrib,data.text) )
	
	#Seccion de gets para todas las cosas	
	def getGameName(self):
		return self._gamename
		
	def getCode(self):
		return self._gamecode
		
	def getVersion(self):
		return self._version
		
	def getBuildDate(self):
		return self._builddate
		
	def getPath(self):
		return self._path
		
	def getClassName(self):
		return self._classname
		
	def getAuthors(self):
		return self._authors
		
	def getServices(self):
		return self._services
		
	def getAdditionalData(self):
		return self._adddata

	def getScreenshots(self):
		return self._screenshots

	def getDescripcion(self):
		return self._description