__author__ = 'LukaAvbreht,SamoKralj'
from tkinter import *

class tkmlin:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=700, height=800)

        plosca = Frame(master,width=700,height=700)
        plosca.grid(row = 1, column = 0, rowspan = 7, columnspan = 7, sticky=N+S+E+W)


        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame, height=2)
        gumb_novaigra.grid(row=0,column=0,sticky=N+S+E+W)

    def newgame(self):
        return "to do"

root = Tk()
root.wm_title('Nine Man\'s Morris')
okno = tkmlin(root)
root.mainloop()