from Tkinter import *
import System.GameList as GL
import System.GameInfo as GI
import System.ArcadeBackendFacade as ABF
from PIL import ImageTk, Image

class ArcadeGUI:
   """Clase que modela una GUI para el arcade"""

   gamecode = None
   root = None
   lista_de_juegos = None

   def cargar_juego(self):
      print("partio el proceso de cargar el juego")
      nombre = self.lista_de_juegos.get(ACTIVE)
      gameinf = None
      root = self.root
      for i in self._back.getGameList().getList():
         
         print(i.getGameName())
         if i.getGameName() == nombre:
            gameinf = i
      if gameinf == None:
         pass

      #JH: Almacenamos gamecode
      self.gamecode = gameinf.getCode()

      #Pedimos screenshots
      print()
      scr = gameinf.getScreenshots()
      for i in scr:
         if i == None:
            i = "Imagenes\omega.gif"

      print("vamos con la primera imagen")
      print(scr[0])
      imgaux = Image.open(scr[0])
      imgaux.thumbnail((600,600), Image.ANTIALIAS)
      img = ImageTk.PhotoImage(imgaux)

      panel = Label(root, image = img, width = 720, height = 400, bg = 'white')
      panel.grid(row=0, column=2, columnspan=4, rowspan=1,sticky=W+E+N+S, padx=5, pady=5)

      print(scr[1])
      print(scr[2])
      imag = Image.open(scr[1])
      imag.thumbnail((200,200), Image.ANTIALIAS)
      img1 = ImageTk.PhotoImage(imag)
      imag2 = Image.open(scr[2])
      imag2.thumbnail((200,200), Image.ANTIALIAS)
      img2 = ImageTk.PhotoImage(imag)
      panel1 = Label(root, image = img1, width = 360, bg = 'black')
      panel1.grid(row=1, column=2, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=5, pady=5)
      panel2 = Label(root, image = img2, width = 360, bg = 'black')
      panel2.grid(row=1, column=3, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=5, pady=5)


      descripcion = Label(root, text=gameinf.getDescripcion(), font=("Lucida Console", 16), fg = "white", bg = "black")
      paneldesc = descripcion
      paneldesc.grid(row = 2, column = 2, columnspan = 3, sticky = W+E+N+S, padx = 5, pady = 5)

   def keyReturnEventHandler(self,event):
      """Metodo encargado de procesar el apretar enter para lanzar un juego"""
      if self.gamecode == None:
         pass
      self._back.LoadGame(self.gamecode)

   def __init__(self, backend):
      self._back = backend
      
      root = Tk()
      self.root = root
      root.configure(background='black')
      root.minsize(1000,1000)
      root.overrideredirect(True)
      root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

      lab = Label()
      lab.config(width = 10, background = 'black')
      lab.grid(row=0, column = 0)


      lista_de_juegos = Listbox(root)
      lista_de_juegos.pack()
      lista_de_juegos.bind('<<ListBoxSelect>>',self.cargar_juego)
      lista_de_juegos.bind("<Return>",self.keyReturnEventHandler)

      lista_de_juegos.config(font = ("Lucida Console", "20"), background = "black", activestyle = 'none', foreground = 'yellow', height = '27')
      for i in self._back.getGameList().getList():
         lista_de_juegos.insert(END, i.getGameName())

      #Dejamos seleccionado uno de los juegos
      lista_de_juegos.selection_set(0)
      lista_de_juegos.activate(0)
      lista_de_juegos.focus_set()
      lista_de_juegos.grid(row=0, column=1, rowspan = '3')
      self.lista_de_juegos = lista_de_juegos
      print("creamos la base de la interfaz")
      self.cargar_juego()



   def go(self):
      self.root.mainloop()
