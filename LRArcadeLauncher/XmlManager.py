#!/usr/local/bin/python
# -*- coding: utf-8 -*-
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
                puntaje.set(str(i),'- 0000')

            self.tree.write('registroArcade.xml')

    def agregarPuntuacion(self, nombreJuego, nombre, puntaje):
        a= self.root.findall(nombreJuego)[0]
        b= a.find('Puntuaciones')
        #for punts in b.items():
        punts = b.items()
        listaDePuntajes = list()
        listaDePuntajes.append((nombre, puntaje))
        for i in range(10):
            listaDePuntajes.append((str(punts[i][1]).split()[0],str(punts[i][1]).split()[1]))

        for i in range(1, len(listaDePuntajes)): 
            for j in range(len(listaDePuntajes)-(len(listaDePuntajes)-i)): 
                if listaDePuntajes[i][1] < listaDePuntajes[j][1]: 
                    temp = listaDePuntajes[i] 
                    listaDePuntajes[i] = listaDePuntajes[j] 
                    listaDePuntajes[j] = temp

        a.remove(b)

        
                

        puntaje = ET.SubElement(a, "Puntuaciones")
        for i in range(10):
            puntaje.set(str(i+1) + '.-',str(listaDePuntajes[i][0])+' '+str(listaDePuntajes[i][1]))
        self.tree.write('registroArcade.xml')
            
                







    
        

        
        

def main():
    xml = XMLManager()
    xml.pedirNombres()
    xml.agregarJuego("Macman", "algunlugar")
    xml.agregarPuntuacion("Macman", "Chiri", 1000)

if __name__ == "__main__":
    main()


