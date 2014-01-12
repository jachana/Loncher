import HighScoreService as HS

def test():
        provider = HS.factory({"max":10,"storage":"internal"},"DEM")
        print("provider inicializado")
        print("Prueba de inicializacion")
        provider.initialize()
        print("Initialize: PASS")
        print("Prueba de tipos")
        print(provider._scorelist)
        print(provider._code)
        print(provider._max)
        print(provider._storage)
        print(provider._tree)
        print(provider._root)
        print(provider._activated)
        print("Fin prueba de tipo")
        print("Prueba de registro")
        import random as r
        for i in range(0,100):
                name = "DE"+str(i)
                score = str(r.randint(0,500000))
                print("Registrando name: "+name+" score: "+str(score))
                provider.register(score,name)
        print("Register: PASS")
        print("Prueba de listado")
        lista = provider.getScores()
        print(lista)
        print("Fin prueba de listado")
        print("Prueba de persistencia")
        provider2 = HS.factory({"max":10,"storage":"internal"},"DEM2")
        provider2.initialize()
        for i in range(0,100):
                name = "DE"+str(i)
                score = str(r.randint(0,500000))
                provider2.register(score,name)
        lista_cre = provider2.getScores()
        provider3 = HS.factory({"max":10,"storage":"internal"},"DEM2")
        lista_de = provider3.getScores()
        print(lista_cre)
        print(lista_de)
        if lista_cre == lista_de:
                print("Listas iguales")
        else:
                print("Listas diferentes")
        print("Fin prueba de persistencia")
        print("Fin de pruebas")

if __name__=="__main__":
        test()
