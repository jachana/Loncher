import HighScoreService as HS

def test():
        provider = HS.factory({"max":10,"storage":"internal"},"DEM")
        print("provider inicializado")
        print("Prueba de inicializacion")
        provider.initialize()
        print("Initialize: PASS")
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
        print("Fin de pruebas")

if __name__=="__main__":
        test()
