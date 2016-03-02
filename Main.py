__author__ = 'LukaAvbreht,SamoKralj'
from tkinter import *
from igra import *

class tkmlin:
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=900, height=700)

        #tuki si bos lahko zbiru kako barva tvoja polja
        self.barva1 = 'Black'
        self.barva2 = 'White'

        #Igralna plosca
        plosca = Canvas(master,width=700,height=700,bg='LemonChiffon')
        plosca.grid(row=0, column=0, rowspan=7, columnspan=7, sticky=N+S+E+W)

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
        self.naredi_figurico(plosca,50,50)
        self.naredi_figurico(plosca,350,50)
        self.naredi_figurico(plosca,650,50)
        self.naredi_figurico(plosca,150,150)
        self.naredi_figurico(plosca,350,150)
        self.naredi_figurico(plosca,550,150)
        self.naredi_figurico(plosca,250,250)
        self.naredi_figurico(plosca,350,250)
        self.naredi_figurico(plosca,450,250)
        self.naredi_figurico(plosca,50,350)
        self.naredi_figurico(plosca,150,350)
        self.naredi_figurico(plosca,250,350)
        self.naredi_figurico(plosca,450,350)
        self.naredi_figurico(plosca,550,350)
        self.naredi_figurico(plosca,650,350)
        self.naredi_figurico(plosca,250,450)
        self.naredi_figurico(plosca,350,450)
        self.naredi_figurico(plosca,450,450)
        self.naredi_figurico(plosca,150,550)
        self.naredi_figurico(plosca,350,550)
        self.naredi_figurico(plosca,550,550)
        self.naredi_figurico(plosca,50,650)
        self.naredi_figurico(plosca,350,650)
        self.naredi_figurico(plosca,650,650)

        #generira gumbe ki niso povezani z igro
        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame)
        gumb_novaigra.grid(row=0, column=9, columnspan=3)

    def newgame(self):
        return "to do"

    def naredi_figurico(self,kam,i,j,barva='Grey'): #none naredi neutralno polje
        kam.create_oval(i-25,j-25,i+25,j+25,fil=barva)

    def klik0(self):
        i = event.x // 50
        j = event.y // 50
        if self.igra.na_potezi == IGRALEC_BELI:
            self.naredi_figurico(plosca,i,j,self.barva2)
        else:
            self.naredi_figurico(plosca,i,j,self.barva1)

    def klik1(self):
        a = event.x // 50
        b = event.y // 50



    def poteza(self, i, j, a=False, b=False): #najprej pogleda v keri fazi smo, pol pa nardi v odvisnosti od tega potezo
        # ce smo v fazi 0 potem je prvi klik le postavljanje kamncka
        # ce smo v drugi fazi usaka poteza zahteva 2 klika
        if self.igra.faza == 0:
            self.klik0
        elif self.igra.faza == 1:
            self.klik1

    def zacni_igro(self,IGRALEC_BELI,IGRALEC_CRNI):
        self.igra = Igra()
        self.igralec_beli = IGRALEC_BELI
        self.igralec_crni = IGRALEC_CRNI

class Igralec():
    def __init__(self,tkmlin):
        self.gui = tkmlin

    def igraj(self):
        pass

    def klik2(self):
        pass #nardit kako izgleda poteza ko se premikamo (figurice)



if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Man\'s Morris')
    okno = tkmlin(root)
    root.mainloop()