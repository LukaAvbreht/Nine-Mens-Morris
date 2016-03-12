__author__ = 'LukaAvbreht,SamoKralj'
from tkinter import *
from igra import *

class tkmlin():
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=900, height=700)
        self.bg = 'LemonChiffon'

        self.igra = Igra()

        #tuki si bos lahko zbiru kako barva tvoja polja
        self.barva1 = 'Black'
        self.barva2 = 'White'

        #Igralnaself.plosca
        self.plosca = Canvas(master, width=700, height=700, bg=self.bg)
        self.plosca.grid(row=0, column=0, rowspan=7, columnspan=7, sticky=N+S+E+W)

        #Slovar ki ima za kljuce id gumbov in jih poveze z poljem v igri
        self.id_polje = dict()

        #crte za igralno plosco
        self.plosca.create_rectangle(50, 50, 650, 650)
        self.plosca.create_rectangle(150, 150, 550, 550)
        self.plosca.create_rectangle(250, 250, 450, 450)

        self.plosca.create_line(350, 50, 350, 250)
        self.plosca.create_line(350, 450, 350, 650)
        self.plosca.create_line(50, 350, 250, 350)
        self.plosca.create_line(450, 350, 650, 350)

        # generira gumbke na polju in jim da svoj id
        for i in range(7):
            for j in range(7):
                if self.igra.plosca[j][i]==None:
                    x =self.plosca.create_oval((100*j+50)-25, (100*i+50)-25, (100*j+50)+25, (100*i+50)+25, outline=self.bg)
                    self.id_polje[x] = (i,j)
        print(self.id_polje)

        self.plosca.bind("<Button-1>", self.klik)

        #stanja za igro
        self.DEFCON1 = 0 #stannje ko je na potezi igralec ter plosca caka na njegov odziv (klik)
        self.DEFCON2 = 0 #stanje ko igra caka na drugi igralcev klik
        self.DEFCON3 = 0 #stanje ko igra caka da igralec izbere zeton ki bi ga rad pobral

        #generira gumbe ki niso povezani z igro
        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame)
        gumb_novaigra.grid(row=0, column=9)

        gumbtest =  Button(master, text="TEST", command= self.test)
        gumbtest.grid(row=1, column=9)

    def test(self):
        if self.DEFCON1 == 0:
            for i in self.id_polje:
                self.plosca.itemconfig(i,fill=self.barva1)
            self.DEFCON1 = 1
        else:
            for i in self.id_polje:
                self.plosca.itemconfig(i,fill=self.barva2)
            self.DEFCON1 = 0


    def klik(self,event):
        """Funkcija ki vrne id polja, na katerega je pritisnil uporabnik"""
        x = event.x
        y = event.y
        kam = self.plosca.find_overlapping(x-25, y-25, x+25, y+25)
        for id in kam:
            if id in self.id_polje:
                print(id)
                return id

    def newgame(self):
        self.igra = Igra()

    def poteza(self, i, j, a=False, b=False): #najprej pogleda v keri fazi smo, pol pa nardi v odvisnosti od tega potezo
        # ce smo v fazi 0 potem je prvi klik le postavljanje kamncka
        # ce smo v drugi fazi usaka poteza zahteva 2 klika
        if self.igra.faza == 0:
            self.klik0
        elif self.igra.faza == 1:
            self.klik1

    def zacni_igro(self, IGRALEC_BELI, IGRALEC_CRNI):
        self.igra = Igra()
        self.igralec_beli = IGRALEC_BELI
        self.igralec_crni = IGRALEC_CRNI

class Igralec():
    """cloveski igralec"""
    def __init__(self, tkmlin):
        """Shrani klike igralca in doloci igralno polje kjer igralec igra igro"""
        self.gui = tkmlin
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

    def ponastavi(self):
        """resetira igrelcevo potezo na nevtralno pozicijo"""
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

    def uporabnikova_poteza(self, event):
        """Metoda ki naredi potezo (preveri njeno veljavnost in naroci igralni plosci da jo zapise v igralno polje)"""
        pass
        # tuki bos meu odvisno od tega u keri fazi si potezo in ti bo preverju ce jo lahko izvede in od tebe zahtevu
        # klike, ko bos kilke izvedu se bo pa poteza zapisala u igro



if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Men\'s Morris')
    okno = tkmlin(root)
    root.mainloop()