import xml.etree.cElementTree as ET
import gameinfo as GI

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
        try:
            self._LoadList(ListPath)
        except Exception:
            pass
        
    def _LoadList(self,ListPath):
        """Metodo que realiza la carga efectiva del archivo"""
        self._tree = ET.ElementTree(None, ListPath)
        root = self._tree.getroot()
        for game in root.findall('Game'):
            jue = GI.GameInfo(game.get('path')) #por cada juego hacemos un GameInfo
            self._games.append(jue)

    def __str__(self):
        buf = "---GameList---\n"
        for game in self._games:
            buf += str(game)+"\n"
        buf +="---END---"
        return buf

    def getList(self):
        """Entrega la lista de objetos GameInfo"""
        return self._games

    def removeByCode(self,code):
        """Remueve un juego dado su codigo del arbol"""
        root = self._tree.getroot()
        for game in root.findall('Game'):
            if GI.GameInfo(game.get('path')).getCode() == code:
                #eliminamos todas las conicidencias
                root.remove(game)
                for r in self._games:
                    if r.getCode() == code:
                        #Quiza quieran sacar este print
                        print("Removed "+str(r))
                        self._games.remove(r)
                
    def saveToXml(self,path):
        """Explicitamente guarda la estructura de arbol actual en un .xml"""
        self._tree.write(path)

    def addGame(self,path):
        """Agrega una entrada al registro"""
        root = self._tree.getroot()
        nuevo = ET.SubElement(root,'Game')
        nuevo.set('path',path)
        

if __name__ == "__main__":
    gl = GameList('GameList_example.xml')
    print(gl)
