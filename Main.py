__author__ = 'LukaAvbreht, SamoKralj'
from tkinter import *
from igra import *
import PIL
from PIL import ImageTk,Image
import threading


class tkmlin():
    def __init__(self,master):
        self.master = master
        self.master.minsize(width=1100, height=700)
        self.bg = 'LightYellow2'  #'LemonChiffon'
        self.zmag_okno = None  #Zmagovalno okno

        #nastavi minimalne sirine stolpcev v polju
        for stolpec in range(11):
            self.master.grid_columnconfigure(stolpec, minsize=100)

        self.igra = Igra()

        #tuki si bos lahko zbiru kako barva tvoja polja
        self.barva1 = 'forest green'
        self.barva1hover = 'yellow green'
        self.barva2 = 'chocolate1'
        self.barva2hover = 'tan1'

        #igralca ki igrata igro
        self.ime_igralec1 = 'Zeleni'
        self.ime_igralec2 = 'Oranžni'

        self.nastavitve_obstraneh(self.ime_igralec1, 1)
        self.nastavitve_obstraneh(self.ime_igralec2, 2)
        
        #kdo je na potezi
        self.na_potezi = None

        #meni za gumbe
        menu = Menu(master)
        master.config(menu=menu)

        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="PvP", command=self.newgame)
        menu_igra.add_command(label="PvAi", command=self.newgamerac)

        menu_test = Menu(menu)
        menu.add_cascade(label="Test", menu=menu_test)
        menu_test.add_command(label="Zmaga", command=self.zmagovalno_okno)


        #Igralnaself.plosca
        self.plosca = Canvas(master, width=700, height=700, bg=self.bg, borderwidth=10, relief=SUNKEN)  #SUNKEN,RAISED
        self.plosca.grid(row=1, column=2, rowspan=7, columnspan=7, sticky=N+S+E+W)

        #Slovar ki ima za kljuce id gumbov in jih poveze z poljem v igri ter obraten slovar
        self.id_polje = dict()
        self.polje_id = dict()

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
                    self.polje_id[(i,j)] = x

        self.plosca.bind("<Button-1>", self.klik)

        self.textbox = StringVar(master, value='Pozdravljeni!')
        Label(self.master, textvariable=self.textbox, font=("Helvetica", 20)).grid(row=0, column=0, columnspan=11)


        #stanja za igro
        self.DEFCON = 0
        #DEFCON 0 : nič, čakamo da začnemo igro
        #DEFCON 1 : Igralec na potezi naj izbere polje
        #DEFCON 2 : Igralec na potezi naj izbere drugo polje
        #DEFCON 3 : Igralec na potezi naj izbere zeton, ki ga bo odstranil
        #DEFCON 4 : Igre je konec, polje je zablokirano,

    def nastavitve_obstraneh(self, ime, st):  #st je lahko 1 ali dva in pomeni katerega igralca nastavljamo
        """Funkcija ki naredi stranske nastavitve na plosci"""
        sprem = int()  #nastavi na katero stran plochs se generira zadeva
        if st == 1:
            sprem=0
        elif st == 2:
            sprem=9
        self.strime = StringVar(self.master, value=ime)
        Label(self.master, textvariable=self.strime, font=("Helvetica", 20)).grid(row=1, column=sprem, columnspan=2)
        self.intzet = IntVar(self.master, value=9)
        Label(self.master, textvariable=self.intzet, font=("Helvetica", 30)).grid(row=2, column=sprem, columnspan=2)

    def nasprotnik(self):
        """Vrne nasprornika."""
        if self.na_potezi == self.igralec1:
            return self.igralec2
        else:
            return self.igralec1

    def zamenjaj_na_potezi(self):
        self.na_potezi = self.nasprotnik()
        if type(self.na_potezi) == Igralec:
            self.na_potezi.ponastavi()
            self.textbox.set("Na potezi je {0}".format(self.na_potezi.ime))
            if len(self.igra.veljavne_poteze()) == 0:
                return self.zmagovalno_okno(self.nasprotnik())
        if type(self.na_potezi) == Racunalnik:
            self.na_potezi.igraj_potezo()



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
            if self.DEFCON in [1,2]: #V primeru, da lahko resetiramo klik
                self.na_potezi.ponastavi()
                self.DEFCON = 1
                if self.igra.faza == 0:
                    self.textbox.set("{0}: Izberi polje kamor želiš postaviti svoj žeton!".format(self.na_potezi.ime))
                else:
                    self.textbox.set("{0}: Izberi svoj žeton!".format(self.na_potezi.ime))
            elif self.DEFCON == 3:
                self.textbox.set("{0}: Vzami nasprotnikov žeton!".format(self.na_potezi.ime))
            else:
                pass

    def zmagovalno_okno(self, zmagovalec = False):
        """Napravi zmagovalno okno, ko se igra zaključi"""
        def unici():
            """Zapre pomozno okno z podatki o zmagi"""
            self.zmag_okno.destroy()
            self.zmag_okno = None

        self.DEFCON = 4
        #zablokiramo polje
        if self.zmag_okno != None:
            self.zmag_okno.lift()
            return
        self.zmag_okno = Toplevel(width=400, height=300)
        self.zmag_okno.title("Zmagovalec")
        self.zmag_okno.resizable(width=False, height=False)
        self.zmag_okno.protocol("WM_DELETE_WINDOW", unici)

        self.zmag_okno.grid_columnconfigure(0, minsize=400)
        #self.zmag_okno.grid_rowconfigure(0, minsize=80)
        #self.zmag_okno.grid_rowconfigure(2, minsize=80)
        besedilo = StringVar(self.zmag_okno)
        Label(self.zmag_okno, textvariable=besedilo, font=("Helvetica", 20)).grid(row=0, column=0)
        if zmagovalec != False:
            message = str("Bravo! Zmagal je igralec " + str(zmagovalec.ime) + "!")
        else:
            message = "Igra ni končana!"
        besedilo.set(message)
        im = Image.open('pokal1.gif')
        photo = ImageTk.PhotoImage(im)
        label = Label(self.zmag_okno, image=photo)
        label.image = photo
        label.grid(row=1, column=0)


    def newgamerac(self):
        """moznosti izbire igre proti racunalniku"""
        self.igra = Igra()
        igralec1 = Igralec(self, self.barva1, self.ime_igralec1)
        igralec2 = Racunalnik(self, self.barva2,self.ime_igralec2,Alpha_betta(1))
        self.nova_igra(igralec1, igralec2)

    def newgame(self):
        """ Nastavi novo igro. """
        self.igra = Igra()
        #igralca
        igralec1 = Igralec(self, self.barva1,self.ime_igralec1)
        igralec2 = Igralec(self, self.barva2,self.ime_igralec2)
        self.nova_igra(igralec1, igralec2)

    def nova_igra(self, igralec1, igralec2):
        """zacne novo igro z dvema igralcema, ki mu jih nastavimo"""
        self.igra = Igra()
        self.igralec1 = igralec1
        self.igralec2 = igralec2
        self.ponastavi()

    def ponastavi(self):
        """pripravi polje za novo igro"""
        for i in self.id_polje:
            self.plosca.itemconfig(i, fill="")
        self.na_potezi = self.igralec1
        self.textbox.set('Na potezi je {}.'.format(self.ime_igralec1))
        self.DEFCON = 1

    def izvedi_potezo(self, id_1=False, id_2=False):
        """Funcija ki izvede potezo ter premakne igralne figure iz polja id_1 na polje id_2"""
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
                self.zamenjaj_na_potezi()
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
                self.zamenjaj_na_potezi()
            

    def vzami_zeton(self, id_1):
        """Funkcija ki se poklice ko igralec doseze mlin. Odstrani figurico iz racunalniskega umesnika in pa iz logike igre"""
        self.plosca.itemconfig(id_1, fill="")
        self.igra.odstrani_figurico(self.id_polje[id_1][0],self.id_polje[id_1][1])
        self.DEFCON = 1
        if self.igra.faza != 0: #PREVERI, ČE SMO ŠTEVILO ŽETONOV IGRALCA SPRAVILI POD 3
            for key, value in self.igra.figurice.items():
                if self.igra.figurice[key] < 3:
                    self.zmagovalno_okno(self.na_potezi)
        self.zamenjaj_na_potezi()

class Igralec():
    """cloveski igralec. primer uporabe znotraj nase igre: self.igralec1 = Igralec(self, 'Black', 'Marjan')"""
    def __init__(self, tkmlin, barva, ime):
        """Shrani klike igralca in doloci igralno polje kjer igralec igra igro"""
        self.gui = tkmlin
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None
        self.barva = barva
        self.ime = ime

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
            self.gui.vzami_zeton(self.tretji_klik)
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
                    self.gui.textbox.set("{0}: Izberi svoj žeton".format(self.ime))
                    
            else:
                #preveri ali je izbran zeton sploh nas
                koord_1 = self.gui.id_polje[self.prvi_klik][0]
                koord_2 = self.gui.id_polje[self.prvi_klik][1]
                if self.gui.igra.plosca[koord_1][koord_2] == self.gui.igra.na_potezi:
                    self.gui.DEFCON = 2
                    id_1 = self.gui.polje_id[(koord_1,koord_2)]
                    self.gui.textbox.set("{0}, izberi kam želiš ta žeton premakniti".format(self.ime))
                    if self.gui.na_potezi.barva == self.gui.barva1:
                        self.gui.plosca.itemconfig(id_1, fill=self.gui.barva1hover)
                    elif self.gui.na_potezi.barva == self.gui.barva2:
                        self.gui.plosca.itemconfig(id_1, fill=self.gui.barva2hover)
                else:
                    self.ponastavi()
                    self.gui.DEFCON = 1
                    self.gui.textbox.set("Nisi izbral svojega žetona. Izberi svoj žeton {0}".format(self.ime))

class Racunalnik():
    def __init__(self, gui, barva, ime, Algoritem):
        self.gui = gui
        self.ime = ime
        self.barva = barva
        self.poteza = None
        self.jemljem = None

        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

        self.algoritem = Algoritem
        self.mislec = None

    def ponastavi(self):
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

    def jemljem(self):
        #racunalnik vse ignorira
        pass

    def uporabnikova_poteza(self):
        #racunalnik vse ignorira
        pass

    def igraj_potezo(self):
        """Racunalnik izvede potezo ki jo pridobi s pomocjo algoritma"""
        self.mislec = threading.Thread(target= lambda: self.algoritem.izracunaj_potezo(self.gui.igra))
        self.mislec.start()
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri ali je algoritem ze izracunal potezo"""
        if self.algoritem.poteza != None:
            if self.algoritem.poteza[2] == False:
                id2 = self.gui.polje_id[(self.algoritem.poteza[0]),(self.algoritem.poteza[1])]
                self.gui.izvedi_potezo(id2)
            else:
                id1 = self.gui.polje_id[(self.algoritem.poteza[2]),(self.algoritem.poteza[3])]
                id2 = self.gui.polje_id[(self.algoritem.poteza[0]),(self.algoritem.poteza[1])]
                self.gui.izvedi_potezo(id1,id2)
            self.mislec = None
            if self.algoritem.jemljem != None:
                id3 = self.gui.polje_id[(self.algoritem.jemljem[0]),(self.algoritem.jemljem[1])]
                self.gui.vzami_zeton(id3)
        else:
            self.gui.plosca.after(100, self.preveri_potezo)
        self.gui.igra.izpisi_plosco()



class Alpha_betta():
    def __init__(self,globina):
        self.globina = globina
        self.igra = None
        self.jaz = None
        self.poteza = None #sem algoritem shrani potezo ko jo naredi
        self.jemljem = None

    def izracunaj_potezo(self,igra):
        self.igra = igra
        self.jaz = self.igra.na_potezi
        self.poteza = self.igra.veljavne_poteze()[0]
        if self.igra.postavljen_mlin((self.poteza[0],self.poteza[1])):
            self.jemljem = self.igra.veljavna_jemanja()[0]
        print(self.poteza,self.jemljem,self.igra.postavljen_mlin((self.poteza[0],self.poteza[1])))


if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Men\'s Morris')
    root.resizable(width=FALSE, height=FALSE)
    okno = tkmlin(root)
    root.mainloop()
