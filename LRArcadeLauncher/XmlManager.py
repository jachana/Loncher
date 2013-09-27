import xml.etree.cElementTree as ET

class XMLManager():
   
    def __init__(self):
        self.tree = ET.ElementTree()

        try:
            self.tree = ET.ElementTree(None,'registroArcade.xml')
            self.root = self.tree.getroot()
            print "intente leer un arbol"

        except Exception:
            self.root = ET.Element("root")
            self.tree = ET.ElementTree(self.root)
            self.tree.write('registroArcade.xml')
            print "intente crear un arbol"
            print Exception.args
            

    def pedirNombres(self):

        nombres = list()

        try:
            for nombre in self.root.findall('Juego'):
                nombres.append(nombre.get('Nombre'))
        except Exception:
            pass
        return nombres

    def agregarJuego(self, nombre, ubicacion):
        nombres = list()
        nombres = self.pedirNombres()
        if nombres.count(nombre) < 1:
            juegoNuevo = ET.SubElement(self.root,'Juego')
            juegoNuevo.set('Nombre',nombre)
            juegoNuevo.set('Ubicacion', ubicacion)
            puntaje = ET.SubElement(juegoNuevo, "Puntuaciones")


            for i in range(11):
                puntaje.set('p' + str(i),'- 0000')

            self.tree.write('registroArcade.xml')

    def quitaJuego(self, nombre):
        a= self.root.findall('Juego')
        b= [x for x in a if x.get('Nombre') == nombre][0]

        self.root.remove(b)
        self.tree.write('registroArcade.xml')



    def agregarRutaImagen(self, nombreJuego, ruta):
        a = self.root.findall('Juego')
        b= [x for x in a if x.get('Nombre') == nombreJuego]
        b[0].set('RutaImagen', ruta)
        self.tree.write('registroArcade.xml')

    def agregarRutaVideo(self, nombreJuego, ruta):
        a = self.root.findall('Juego')
        b= [x for x in a if x.get('Nombre') == nombreJuego]
        b[0].set('RutaVideo', ruta)
        self.tree.write('registroArcade.xml')

    def agregarDescripcion(self, nombreJuego, desc):
        a = self.root.findall('Juego')
        b= [x for x in a if x.get('Nombre') == nombreJuego]
        b[0].set('Descripcion', desc)
        self.tree.write('registroArcade.xml')

    def getDescripcion(self, nombreJuego):
        descripcion = "No hay descripcion disponible"
        a = self.root.findall('Juego')
        b= [x for x in a if x.get('Nombre') == nombreJuego]

        try:
            if b[0].get('Descripcion') != None:
                descripcion = b[0].get('Descripcion')
            return descripcion
        
        except Exception:
            return descripcion
     
            



    def agregarPuntuacion(self, nombreJuego, nombre, puntaje):
        a= self.root.findall('Juego')
        b= [x for x in a if x.get('Nombre') == nombreJuego]
        #for punts in b.items():
        c=b[0].find('Puntuaciones')
        punts = c.items()
        listaDePuntajes = list()
        listaDePuntajes.append((nombre, puntaje))
        for i in range(10):
            listaDePuntajes.append((str(punts[i][1]).split()[0],int(str(punts[i][1]).split()[1])))

        
        listaDePuntajes.sort(key=lambda tup: tup[1])
        listaDePuntajes.reverse()

        b[0].remove(c)

        
                

        puntaje = ET.SubElement(b[0], "Puntuaciones")
        for i in range(len(listaDePuntajes) -1):
            puntaje.set('p' + str(i) + '.-',str(listaDePuntajes[i][0])+' '+str(listaDePuntajes[i][1]))
        self.tree.write('registroArcade.xml')
            
                



        
        

def main():
    xml = XMLManager()
    xml.pedirNombres()
    
    xml.agregarJuego("Macman", "algunlugar")
    xml.agregarPuntuacion("Macman", "Chiri", 1000)
    xml.agregarRutaImagen("Macman", "lala.jpg")
    xml.getDescripcion("Macman")
    xml.quitaJuego("Macman")

if __name__ == "__main__":
    main()

