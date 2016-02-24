__author__ = 'AvbrehtL14'
from tkinter import *
#from tkinter.filedialog import *

class tkmlin:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=600, height=600)

    def help(self):
        window = Toplevel()
        window.title("Pomoc")
        window.minsize(width=180, height=140)
        text = Message(window,text=
        """Izberite tekstovno datoteko, v kateri je v vsaki vrstici vektor oblike = [A1,A2,A3....An], teh vektorjev pa naj bo n \n
        """)
        text.grid(column=0,row=0)
        gumb_zapri = Button(window, text = "OK", command= window.destroy)
        gumb_zapri.grid(column=0,row=1)

root = Tk()
root.wm_title('Nine Man\'s Morris')
okno = tkmlin(root)
root.mainloop()