#Clase que modela la información que expone un juego, se carga desde un GameInfo.xml
import xml.etree.cElementTree as ET
import os

class GameInfo:
	def __init__(self,XmlPath):
		"""Crea un objeto que represneta la info de un juego"""
		self.tree = ET.ElementTree()
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
		self.loadXml(XmlPath)
		
	def loadXml(self,XmlPath):
		"""Carga la información desde un archivo"""
		#TODO: Cragar datos desde el Xml
		pass
		
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
	
	