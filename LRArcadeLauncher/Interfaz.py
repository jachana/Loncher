from Tkinter import *
import XmlManager
from PIL import ImageTk, Image


def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()



   
root = Tk()
root.configure(background='black')
root.minsize(1000,1000)
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

lab = Label()
lab.config(width = 10, background = 'black')
lab.grid(row=0, column = 0)


listaDeJuegos = Listbox(root)
listaDeJuegos.pack()

xml = XMLManager.XMLManager()
listaDeJuegos.config(font = ("Lucida Console", "20"), background = "black", activestyle = 'none', foreground = 'yellow', height = '27')
listaDeNombres = xml.pedirNombres()


for i in listaDeNombres:
    
    listaDeJuegos.insert(END, i)

listaDeJuegos.selection_set(0)
listaDeJuegos.activate(0)
listaDeJuegos.focus_set()
listaDeJuegos.grid(row=0, column=1, rowspan = '3')

imgaux = Image.open("omega.jpg")
imgaux.thumbnail((600,600), Image.ANTIALIAS)
img = ImageTk.PhotoImage(imgaux)

panel = Label(root, image = img, width = 720, height = 400, bg = 'white')
panel.grid(row=0, column=2, columnspan=4, rowspan=1,sticky=W+E+N+S, padx=5, pady=5)


imag = Image.open("omega.jpg")
imag.thumbnail((200,200), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(imag)
panel1 = Label(root, image = img1, width = 360, bg = 'blue')
panel1.grid(row=1, column=2, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=5, pady=5)
panel2 = Label(root, image = img1, width = 360, bg = 'blue')
panel2.grid(row=1, column=3, columnspan=1, rowspan=1,sticky=W+E+N+S, padx=5, pady=5)


descripcion = Label(root, text="Soy una descripcion", font=("Lucida Console", 16), fg = "white", bg = "black")
paneldesc = descripcion
paneldesc.grid(row = 2, column = 2, columnspan = 3, sticky = W+E+N+S, padx = 5, pady = 5)

""" 
button1.grid(row=2, column=2)
button2.grid(row=2, column=3)
"""



root.mainloop()
