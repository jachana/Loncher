#Clase que contiene la infromacion relevante de un ball

class BallInfo():
	"""Contiene la informacion relevante de un archivo ball.
	"""

	def __init__(self):
		self.ballltype = "generic"
		self.authname = "AuthoGen"
		self.pkgname = "nopkg"
		self.dependencies = []
		self.pkgver = 0

	def __init__(self,path):
		self.__init__()
		self.load_info(path)

	def load_info(self,path):
		pass

	def write_info(self,path):
		pass

	def get_balltype(self):
		return self.ballltype

	def get_authname(self):
		return self.authname

	def get_pkgname(self):
		return self.pkgname

	def get_dependencies(self):
		return self.dependencies

	def get_pkgver(self):
		return self.pkgver

	def set_balltype(self,value):
		self.ballltype = value

	def set_authname(self,value):
		self.authname = value

	def set_pkgname(self,value):
		self.pkgname = value

	def set_pkgver(self,value):
		self.pkgver = value

	def set_dependencies(self,value):
		self.dependencies = value
