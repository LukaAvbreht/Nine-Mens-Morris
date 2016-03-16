__author__ = 'LukaAvbreht,SamoKralj'
from tkinter import *
from igra import *

class tkmlin():
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=900, height=700)
        self.bg = 'LightYellow2'  #'LemonChiffon'

        self.igra = Igra()

        #tuki si bos lahko zbiru kako barva tvoja polja
        self.barva1 = 'forest green'
        self.barva2 = 'chocolate1'

        #igralca ki igrata igro
        self.ime_igralec_crni = 'Črni'
        self.ime_igralec_beli = 'Beli'

        #igralca
        self.igralec_crni = Igralec(self, self.barva1)
        self.igralec_beli = Igralec(self, self.barva2)
        
        #kdo je na potezi
        self.na_potezi = None

        #Igralnaself.plosca
        self.plosca = Canvas(master, width=700, height=700, bg=self.bg, borderwidth=10)
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
                    x =self.plosca.create_oval((100*j+50)-25, (100*i+50)-25, (100*j+50)+25, (100*i+50)+25, outline="")
                    self.id_polje[x] = (i,j)

        self.plosca.bind("<Button-1>", self.klik)

        self.textbox = StringVar(master, value='Pozdravljeni!')
        Label(self.master, textvariable=self.textbox, font=("Helvetica", 20)).grid(row=0, column=0, columnspan=7)


        #stanja za igro
        self.DEFCON = 0
        #DEFCON 0 : nič, čakamo da začnemo igro
        #DEFCON 1 : Igralec na potezi naj izbere polje
        #DEFCON 2 : Igralec na potezi naj izbere drugo polje
        #DEFCON 3 : Igralec na potezi naj izbere zeton, ki ga bo odstranil
        #DEFCON 4 : Igre je konec, polje je zablokirano,
        
        #generira gumbe ki niso povezani z igro
        gumb_novaigra = Button(master, text="Nova igra", command= self.newgame)
        gumb_novaigra.grid(row=0, column=9, sticky=N+W+E+S)

    #################################################################################
    #trol
        gumbtest = Button(master, text="TEST", command= self.test)
        gumbtest.grid(row=0, column=10, sticky=N+W+E+S)

        gumbtest2 = Button(master, text="Kao Zmaga", command=self.zmagovalno_okno)
        gumbtest2.grid(row=0, column=11, sticky=N+W+E+S)

        gumbtest3 = Button(master, text="test2", command=self.test2())
        gumbtest3.grid(row=0, column=12, sticky=N+W+E+S)

    def test(self):
        if self.DEFCON == 0:
            for i in self.id_polje:
                self.plosca.itemconfig(i,fill=self.barva1)
            self.textbox.set('Na potezi je {}.'.format(self.ime_igralec_beli))
            self.DEFCON = 1
        else:
            for i in self.id_polje:
                self.plosca.itemconfig(i,fill=self.barva2)
            self.textbox.set('Na potezi je {}.'.format(self.ime_igralec_crni))
            self.DEFCON = 0

    def test2(self):
        print(self.igra.veljavne_poteze())
    ##################################################################################

    def klik(self,event):
        """Funkcija ki vrne id polja, na katerega je pritisnil uporabnik"""
        x = event.x
        y = event.y
        kam = self.plosca.find_overlapping(x-25, y-25, x+25, y+25)
        znacka = False
        for id in kam:
            if id in self.id_polje:
                znacka = True #nam pove, da smo zadeli nekaj
                if self.DEFCON == 0:
                    self.textbox.set("Klikni gumb NOVA IGRA")
                elif self.DEFCON == 1:
                    self.na_potezi.prvi_klik = id
                    self.na_potezi.uporabnikova_poteza()
                elif self.DEFCON == 2:
                    self.na_potezi.drugi_klik = id
                    self.na_potezi.uporabnikova_poteza()
                elif self.DEFCON == 3:
                    self.na_potezi.tretji_klik = id
                    self.na_potezi.jemljem()
                elif self.DEFCON == 4:
                    self.textbox.set("Igre je konec. Za novo igro pritisni gumb NOVA IGRA.")
                    znacka = True #Ker so vsi kliki ignorirani!
                else:
                    pass
        if znacka == False: #kliknili smo kar nekam, resetirajmo na zacetek poteze
            self.na_potezi.ponastavi()
            self.DEFCON = 1
            self.textbox.set("{0}: Izberi svoj žeton".format(self.na_potezi.barva))

    #Trenutno zmagovalno okno odpre kar nekje in ni lepega izgleda!
    def zmagovalno_okno(self, zmagovalec = False):
        self.DEFCON = 4
        #zablokiramo polje
        
        pop_up = Toplevel(height = 500, width = 500)
        pop_up.title("Zmagovalec")
        

        besedilo = Message(pop_up, text = str("Bravo! Zmagal je igralec " + str(zmagovalec) + "!"))
        besedilo.pack()
        
    def newgame(self):
        self.igra = Igra()
        for i in self.id_polje:
            self.plosca.itemconfig(i, fill=None)
        self.na_potezi = self.igralec_crni
        self.textbox.set('Na potezi je {}.'.format(self.ime_igralec_crni))
        self.DEFCON = 1

    def izvedi_potezo(self, id_1=False, id_2=False):
        """Funcija ki izvede potezo ter premakne igralne figure"""
        if id_1 != False:
            prvopolje = self.id_polje[id_1]
        if id_2 != False:
            drugopolje = self.id_polje[id_2]
        if id_1 != False and id_2 == False:
            self.plosca.itemconfig(id_1, fill=self.na_potezi.barva)
            self.igra.poteza(prvopolje[0], prvopolje[1])
            if self.igra.postavljen_mlin(prvopolje):
                self.DEFCON = 3
                self.textbox.set("Izberi zeton, ki ga bos pobral")
            else:
                if self.na_potezi == self.igralec_crni:
                    self.na_potezi = self.igralec_beli
                    self.textbox.set('Na potezi je {}.'.format(self.ime_igralec_beli))
                else:
                    self.na_potezi = self.igralec_crni
                    self.textbox.set('Na potezi je {}.'.format(self.ime_igralec_crni))
        else:
            self.plosca.itemconfig(id_1, fill="")
            self.plosca.itemconfig(id_2, fill=self.na_potezi.barva)
            self.igra.poteza(drugopolje[0], drugopolje[1], prvopolje[0], prvopolje[1])
            if self.igra.postavljen_mlin(drugopolje): #zahtevamo, da pobere žeton
                self.DEFCON = 3
                self.textbox.set("Izberi žeton, ki ga boš pobral!")
            else:
                #se pripravimo na naslednjo potezo
                self.DEFCON = 1
                if self.na_potezi == self.igralec_crni:
                    self.na_potezi = self.igralec_beli
                else:
                    self.na_potezi = self.igralec_crni
                self.textbox.set("Izberi polje {0}".format(self.na_potezi.barva))
                self.na_potezi.ponastavi()
            

    def vzami_zeton(self, id_1, i, j):
        self.plosca.itemconfig(id_1, fill="")
        self.igra.odstrani_figurico(i, j)
        self.DEFCON = 1
        if self.igra.faza != 0: #PREVERI, ČE SMO ŠTEVILO ŽETONOV IGRALCA SPRAVILI POD 3
            for key, value in self.igra.figurice.items():
                if self.igra.figurice[key] < 3:
                    self.zmagovalno_okno(self.na_potezi)
        if self.na_potezi == self.igralec_crni:
            self.na_potezi = self.igralec_beli
        else:
            self.na_potezi = self.igralec_crni
        self.na_potezi.ponastavi()
        self.textbox.set("Na potezi je {0}".format(self.na_potezi.barva))


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

    def jemljem(self):
        """Preveri, če lahko izbrani žeton odstranimo. """
        koord_1 = self.gui.id_polje[self.tretji_klik][0]
        koord_2 = self.gui.id_polje[self.tretji_klik][1]
        if self.gui.igra.lahko_jemljem(koord_1, koord_2):
            self.gui.vzami_zeton(self.tretji_klik, koord_1, koord_2)
        else:
            self.ponastavi()
            self.gui.textbox.set("Izberi žeton, ki ga smeš vzeti!")
            

    def uporabnikova_poteza(self):
        """Metoda ki naredi potezo (preveri njeno veljavnost in naroci igralni plosci da jo zapise v igralno polje)"""
        if self.gui.igra.faza == 0:
            koord_1 = self.gui.id_polje[self.prvi_klik][0]
            koord_2 = self.gui.id_polje[self.prvi_klik][1]
            if self.gui.igra.je_veljavna(koord_1, koord_2):
                self.gui.izvedi_potezo(self.prvi_klik)
        else:
            if self.drugi_klik != None:
                koord_1 = self.gui.id_polje[self.prvi_klik][0]
                koord_2 = self.gui.id_polje[self.prvi_klik][1]
                koord_3 = self.gui.id_polje[self.drugi_klik][0]
                koord_4 = self.gui.id_polje[self.drugi_klik][1]
                if self.gui.igra.je_veljavna(koord_3, koord_4, koord_1, koord_2):
                    self.gui.izvedi_potezo(self.prvi_klik, self.drugi_klik)
                else:
                    #nismo izvedli veljavne poteze, vrnemo se na zacetek poteze!
                    self.ponastavi()
                    self.gui.DEFCON = 1
                    self.gui.textbox.set("{0}: Izberi svoj žeton".format(self.barva))
                    
            else:
                #preveri ali je izbran zeton sploh nas
                koord_1 = self.gui.id_polje[self.prvi_klik][0]
                koord_2 = self.gui.id_polje[self.prvi_klik][1]
                if self.gui.igra.plosca[koord_1][koord_2] == self.gui.igra.na_potezi:
                    self.gui.DEFCON = 2
                    self.gui.textbox.set("Izberi kam želiš ta žeton premakniti")
                else:
                    self.ponastavi()
                    self.gui.DEFCON = 1
                    self.gui.textbox.set("Nisi izbral svojega žetona. Izberi svoj žeton {0}".format(self.barva))


if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Men\'s Morris')
    root.resizable(width=FALSE, height=FALSE)
    okno = tkmlin(root)
    root.mainloop()
