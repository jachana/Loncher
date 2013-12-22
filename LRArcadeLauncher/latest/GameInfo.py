#Clase que modela la informacion que expone un juego, se carga desde un GameInfo.xml
import xml.etree.cElementTree as ET
import os

class GameInfo:
	def __init__(self,XmlPath):
		"""Crea un objeto que represneta la info de un juego"""
		self._tree = ET.ElementTree()
		self._gamename = "Juego"
		self._gamecode = "G0"
		self._version = 001
		self._builddate = "01-01-2014"
		self._description = "Descripcion"
		self._path = "./StartBase.py"
		self._classname = "Start"
		self._authors = []
		self._services = []
		self._adddata = []
		self._screenshots = []
		if XmlPath != '':
			self.loadXml(XmlPath)
		
	def __str__(self):
		return str(self._gamename)+"("+str(self._gamecode)+") ver "+str(self._version)+"("+str(self._builddate)+") on "+str(self._path)+"("+str(self._classname)+") by "+str(self._authors)+" uses "+str(self._services)
		
	def loadXml(self,XmlPath):
		"""Carga la informacion desde un archivo"""
		#TODO: Cragar datos desde el Xml
		self._tree = ET.ElementTree(None,XmlPath)
		root = self._tree.getroot()
		#Leemos datos basicos desde el Xml
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
				self._services.append( (service.get('name'),service.attrib) )
		#Finalmente cargamos los autores y la data adicional
		for authors in root.findall('Authors'):
			for author in authors.findall('Author'):
				self._authors.append(author.get('name'))
		for adddata in root.findall('AdditionalData'):
			for data in adddata:
				self._adddata.append( (data.tag,data.attrib,data.text) )
		
	def getGameName(self):
		return self._gamename
		
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
	
	
