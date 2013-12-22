import xml.etree.cElementTree as ET
import GameInfo as GI

class GameList:
    """Clase que representa la lista de juegos del arcade"""
    
    def __init__(self):
        """Intenta cargar una lista desde GameList.xml"""
        self._tree = ET.ElementTree()
        self._games = []
        try:
            self._LoadList('GameList.xml')
        except Exception:
            pass
        
    def __init__(self,ListPath):
        """Carga una lista desde el path proporcionado"""
        self._tree = ET.ElementTree()
        self._games = []
        self._LoadList(ListPath)
        
    def _LoadList(self,ListPath):
        """Metodo que realiza la carga efectiva del archivo"""
        self._tree = ET.ElementTree(None, ListPath)
        root = self._tree.getroot()
        for game in root.findall('Game'):
            jue = GI.GameInfo(game.get('path'))
            self._games.append(jue)

    def __str__(self):
        buf = "---GameList---\n"
        for game in self._games:
            buf += str(game)+"\n"
        buf +="---END---"
        return buf

if __name__ == "__main__":
    gl = GameList('GameList_example.xml')
    print(gl)
