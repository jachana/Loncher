#Shell del arcade
#La idea es tener algo mas poderoso que la CLI que hay, que sea extensible

import tools.logger

class ArcadeSH:
	"""Clase que implementa interfaz shell del arcade.
	"""

	def __init__(self,back):
		self._back = back
		self._log = tools.logger.get_logger()

	def go(self):
		"""Metodo que pone en ejecucion la interfaz.
		"""

		pass
