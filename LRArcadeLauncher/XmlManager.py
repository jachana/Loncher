import xml.etree.cElementTree as ET

class XMLManager():
   
    def __init__(self):

        try:
            self.tree = ET.parse('registroArcade.xml')
            self.root = self.tree.getroot()
            print "intente leer un arbol"

        except Exception:
            self.root = ET.Element("root")
            self.tree = ET.ElementTree(self.root)
            self.tree.write('registroArcade.xml')
            print "intente crear un arbol"
            

    def pedirNombres(self):

        nombres = list()

        try:
            for nombre in self.root.findall('Nombre'):
                nombres.append(nombre)
        except Exception:
            pass
        return nombres

    def agregarJuego(self, nombre, ubicacion):
        nombres = list()
        nombres = self.pedirNombres()
        if nombres.count(nombre) < 1:
            juegoNuevo = ET.SubElement(self.root,nombre)
            juegoNuevo.set('Nombre',nombre)
            juegoNuevo.set('Ubicacion', ubicacion)
            puntaje = ET.SubElement(juegoNuevo, "Puntuaciones")


            for i in range(10):
                puntajes = ET.SubElement(puntaje, str(i+1)+'.-')
                puntajes.set('-','- 0000')

            self.tree.write('registroArcade.xml')

    def agregarPuntuacion(self, nombreJuego, nombre, puntaje):
        
        for punts in self.root.findall('Puntuaciones'):
            listaDePuntajes = list()
            for i in range(len(10)):
                listaDePuntajes.append((i,str(punts.findall(i + '.-')).split()))
            listaDePuntajes.sort()
                
        
        

def main():
    xml = XMLManager()
    xml.pedirNombres()
    xml.agregarJuego("Macman", "algunlugar")

if __name__ == "__main__":
    main()