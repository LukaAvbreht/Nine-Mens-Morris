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

        #igralca ki igrata igro
        self.ime_igralec1 = 'Črni'
        self.ime_igralec2 = 'Beli'

        #igralca
        self.igralec_beli = Igralec(self, self.barva2)
        self.igralec_crni = Igralec(self, self.barva1)

        #kdo je na potezi
        self.na_potezi = None

        #Igralnaself.plosca
        self.plosca = Canvas(master, width=700, height=700, bg=self.bg)
        self.plosca.grid(row=1, column=0, rowspan=7, columnspan=7, sticky=N+S+E+W)

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

        self.textbox = StringVar(master, value='Pozdravljeni!')
        Label(self.master, textvariable=self.textbox, font=("Helvetica", 20)).grid(row=0, column=0, columnspan=7)

        #stanja za igro
        self.DEFCON = 0
        #DEFCON 0 : nič, čakamo da začnemo igro
        #DEFCON 1 : Igralec na potezi naj izbere polje
        #DEFCON 2 : Igralec na potezi naj izbere drugo polje
        #DEFCON 3 : Igralec na potezi naj izbere zeton, ki ga bo odstranil

        #generira gumbe ki niso povezani z igro
        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame)
        gumb_novaigra.grid(row=0, column=9, sticky=N+W+E+S)

        gumbtest =  Button(master, text="TEST", command= self.test)
        gumbtest.grid(row=0, column=10, sticky=N+W+E+S)
    
    #trol
    def test(self):
        if self.DEFCON == 0:
            for i in self.id_polje:
                self.plosca.itemconfig(i,fill=self.barva1)
            self.textbox.set('Na potezi je {}.'.format(self.ime_igralec2))
            self.DEFCON = 1
        else:
            for i in self.id_polje:
                self.plosca.itemconfig(i,fill=self.barva2)
            self.textbox.set('Na potezi je {}.'.format(self.ime_igralec1))
            self.DEFCON = 0

    def klik(self,event):
        """Funkcija ki vrne id polja, na katerega je pritisnil uporabnik"""
        x = event.x
        y = event.y
        kam = self.plosca.find_overlapping(x-25, y-25, x+25, y+25)
        for id in kam:
            if id in self.id_polje:
                if self.DEFCON == 0:
                    self.textbox.set("Klikni gumb NOVA IGRA")
                elif self.DEFCON == 1:
                    self.na_potezi.prvi_klik = id
                    poteza = self.na_potezi.uporabnikova_poteza()
                elif self.DEFCON == 2:
                    pass
                elif self.DEFCON == 3:
                    pass
                else:
                    pass

    def newgame(self):
        self.igra = Igra()
        for i in self.id_polje:
            self.plosca.itemconfig(i, fill=None)
        self.na_potezi = self.igralec_crni
        self.textbox.set('Na potezi je {}.'.format(self.ime_igralec1))
        self.DEFCON = 1

    def poteza(self, i, j, a=False, b=False): #najprej pogleda v keri fazi smo, pol pa nardi v odvisnosti od tega potezo
        # ce smo v fazi 0 potem je prvi klik le postavljanje kamncka
        # ce smo v drugi fazi usaka poteza zahteva 2 klika
        if self.igra.faza == 0:
            self.klik0
        elif self.igra.faza == 1:
            self.klik1

    def izvedi_potezo(self, id_1 = False, id_2 = False, id_3 = False):
        print(self.na_potezi.barva)
        if id_1 != False:
            prvopolje = self.id_polje[id_1]
        if id_2 != False:
            drugopolje = self.id_polje[id_2]
        if id_3 != False:
            tretjepolje = self.id_polje[id_3]
        if id_1 != False and ((id_2, id_3) == (False, False)):
            self.plosca.itemconfig(id_1, fill = self.na_potezi.barva)
            self.igra.poteza(prvopolje[0],prvopolje[1])
            print("sem tukaj")
            if self.na_potezi == self.igralec_crni:
                print("DA?")
                self.na_potezi = self.igralec_beli
            else:
                self.na_potezi = self.igralec_crni
        elif id_3 == False:
            pass
        else:
            #tudi poberemo zeton
            pass

class Igralec():
    """cloveski igralec"""
    def __init__(self, tkmlin, barva):
        """Shrani klike igralca in doloci igralno polje kjer igralec igra igro"""
        self.gui = tkmlin
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None
        self.barva = barva

    def ponastavi(self):
        """resetira igrelcevo potezo na nevtralno pozicijo"""
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

    def uporabnikova_poteza(self):
        """Metoda ki naredi potezo (preveri njeno veljavnost in naroci igralni plosci da jo zapise v igralno polje)"""
        if self.gui.igra.faza == 0:
            koord_1 = self.gui.id_polje[self.prvi_klik][0]
            koord_2 = self.gui.id_polje[self.prvi_klik][1]
            if self.gui.igra.je_veljavna(koord_1, koord_2):
                self.gui.izvedi_potezo(self.prvi_klik)
        else:
            pass
        # tuki bos meu odvisno od tega u keri fazi si potezo in ti bo preverju ce jo lahko izvede in od tebe zahtevu
        # klike, ko bos kilke izvedu se bo pa poteza zapisala u igro



if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Men\'s Morris')
    root.resizable(width=FALSE, height=FALSE)
    okno = tkmlin(root)
    root.mainloop()
