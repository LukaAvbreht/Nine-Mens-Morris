__author__ = 'LukaAvbreht,SamoKralj'
from tkinter import *

class tkmlin:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=700, height=700)

        #Igralna plosca
        plosca = Canvas(master,width=700,height=700)
        plosca.grid(row = 0, column = 0, rowspan = 7, columnspan = 7, sticky=N+S+E+W)

        #crte za igralno plosco
        plosca.create_line(50,50,650,50)
        plosca.create_line(50,650,650,650)
        plosca.create_line(50,50,50,650)
        plosca.create_line(650,50,650,650)

        plosca.create_line(150,150,550,150)
        plosca.create_line(550,150,550,550)
        plosca.create_line(150,150,150,550)
        plosca.create_line(150,550,550,550)

        plosca.create_line(250,250,450,250)
        plosca.create_line(450,250,450,450)
        plosca.create_line(250,250,250,450)
        plosca.create_line(250,450,450,450)

        plosca.create_line(350,50,350,250)
        plosca.create_line(350,450,350,650)
        plosca.create_line(50,350,250,350)
        plosca.create_line(450,350,650,350)

        #Gumpki namenjeni za igro

        #generira gumbe ki niso povezani z igro
        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame, height=2)
        gumb_novaigra.grid(row=0,column=7,sticky=N+S+E+W)

    def newgame(self):
        return "to do"

if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Man\'s Morris')
    okno = tkmlin(root)
    root.mainloop()