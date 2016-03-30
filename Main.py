__author__ = 'LukaAvbreht, SamoKralj'
from tkinter import *
from igra import *
from PIL import ImageTk,Image
import threading
import random

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

        self.igralec1 = None
        self.igralec2 = None

        self.nastavitve_obstraneh(self.ime_igralec1, 1)
        self.nastavitve_obstraneh(self.ime_igralec2, 2)

        self.canvas1 = Canvas(master, width=200, height=400)  #,bg=self.bg)
        self.canvas2 = Canvas(master, width=200, height=400)  #,bg=self.bg)
        self.canvas1.grid(row=3, column=0, columnspan=2, sticky=N+S+E+W)
        self.canvas2.grid(row=3, column=9, columnspan=2, sticky=N+S+E+W)

        self.play1ids = []
        self.play2ids = []

        #kdo je na potezi
        self.na_potezi = None  #to je treba narest da je sam enkrat kdo je na potezi in to je self.igra.na_potezi

        #meni za gumbe
        menu = Menu(master)
        master.config(menu=menu)

        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="PvP", command=self.newgame)
        menu_igra.add_command(label="PvAi", command=self.newgamerac)
        menu_igra.add_command(label="Nova igra", command=self.izbira_nove_igre)
        menu_igra.add_command(label="Izpisi_plosco", command = self.izpisi)

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

    def postavi_stranske(self):
        slovarzanastran = [(134, 30), (66, 98), (134, 98), (66, 166), (134, 166), (66, 234), (134, 234), (66, 302), (134, 302)]
        for j in slovarzanastran:
            x = self.canvas1.create_oval(j[0]-25, j[1]-25, j[0]+25, j[1]+25, outline="", fill=self.barva1)
            self.play1ids.append(x)
        for j in slovarzanastran:
            x = self.canvas2.create_oval(j[0]-25, j[1]-25, j[0]+25, j[1]+25, outline="", fill=self.barva2)
            self.play2ids.append(x)

    def izpisi(self):
        self.igra.izpisi_plosco()

    def nastavitve_obstraneh(self, ime, st):  #st je lahko 1 ali dva in pomeni katerega igralca nastavljamo
        """Funkcija ki naredi stranske nastavitve na plosci"""
        sprem = int()  #nastavi na katero stran plochs se generira zadeva
        if st == 1:
            sprem=0
        elif st == 2:
            sprem=9
        self.strime = StringVar(self.master, value=ime)
        Label(self.master, textvariable=self.strime, font=("Helvetica", 20)).grid(row=1, column=sprem, columnspan=2)
        #self.intzet = IntVar(self.master, value=9)
        #Label(self.master, textvariable=self.intzet, font=("Helvetica", 30)).grid(row=2, column=sprem, columnspan=2)

    def nasprotnik(self):  #to ko popravma bo vrjent neuporabno
        """Vrne nasprornika."""
        if self.na_potezi == self.igralec1:
            return self.igralec2
        else:
            return self.igralec1

    def zamenjaj_na_potezi(self):  #to se mora zgodit v igri
        if self.igra.na_potezi == IGRALEC_ENA:
            self.na_potezi = self.igralec1
        else:
            self.na_potezi = self.igralec2
        if len(self.igra.veljavne_poteze()) == 0:
                return self.zmagovalno_okno(self.nasprotnik())
        self.textbox.set("Na potezi je {0}".format(self.na_potezi.ime))
        if type(self.na_potezi) == Igralec:
            self.na_potezi.ponastavi()
        elif type(self.na_potezi) == Racunalnik:
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
                self.DEFCON = 1
                if self.igra.faza == 0:
                    self.textbox.set("{0}: Izberi polje kamor želiš postaviti svoj žeton!".format(self.na_potezi.ime))
                else:
                    self.textbox.set("{0}: Izberi svoj žeton!".format(self.na_potezi.ime))
                    if self.na_potezi.prvi_klik != None:
                        self.plosca.itemconfig(self.na_potezi.prvi_klik, fill=self.na_potezi.barva)
                self.na_potezi.ponastavi()
            elif self.DEFCON == 3:
                self.textbox.set("{0}: Vzami nasprotnikov žeton!".format(self.na_potezi.ime))
            elif self.DEFCON == 4:
                pass
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
        self.play1ids = []
        self.play2ids = []
        self.postavi_stranske()

    def izbira_nove_igre(self):
        """Napravi okno, kjer si lahko izberemo nastavitve za novo igro, ter jo tako zacnemo"""

        def creategame():
            """Pomozna funkcija ki naredi novo igro"""
            self.ime_igralec1 = ime1.get()
            self.ime_igralec2 = ime2.get()
            if igralec1_clovek.get():
                igralec1 = Igralec(self, self.barva1, self.ime_igralec1)
            else:
                igralec1 = Racunalnik(self, self.barva1, self.ime_igralec1, Alpha_betta(1))
            if igralec2_clovek.get():
                igralec2 = Igralec(self, self.barva2, self.ime_igralec2)
            else:
                igralec2 = Racunalnik(self, self.barva2, self.ime_igralec2, Alpha_betta(1))
            self.nova_igra(igralec1,igralec2)
            nov_game.destroy()



        #ustvari novo okno
        nov_game = Toplevel()
        nov_game.grab_set()
        nov_game.title('Nine Men\'s Morris - nova igra')     #nastavi ime okna
        nov_game.resizable(width=False, height=False)

        for stolpec in range(4):
            nov_game.grid_columnconfigure(stolpec, minsize=100)

        Label(nov_game, text='Nastavitve nove igre', font=('Times',20)).grid(column=0, row=0, columnspan=5)

        #nastavitve igralcev
        Label(nov_game, text='Igralec 1', font=('Times',12)).grid(column=1, row=1)
        Label(nov_game, text='Igralec 2', font=('Times',12)).grid(column=3, row=1)
        Label(nov_game, text="Tip igralca:").grid(row=2, column=0, rowspan=2, sticky="E")
        Label(nov_game, text="Tip igralca:").grid(row=2, column=2, rowspan=2, sticky="E")

        igralec1_clovek = BooleanVar()
        igralec1_clovek.set(True)
        igralec2_clovek = BooleanVar()
        igralec2_clovek.set(True)
        igralci = [("Človek", True, igralec1_clovek, 3, 1), ("Računalnik", False, igralec1_clovek, 4, 1),
                   ("Človek", True, igralec2_clovek, 3, 3), ("Računalnik", False, igralec2_clovek, 4, 3)]

        for besedilo, vrednost, spremenljivka, vrstica, stolpec in igralci:
            Radiobutton(nov_game, text=besedilo, variable=spremenljivka, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica, column=stolpec)

        Label(nov_game, text="Ime igralca:").grid(row=5, column=0, sticky="E")
        Label(nov_game, text="Ime igralca:").grid(row=5, column=2, sticky="E")

        ime1 = Entry(nov_game, font=('Times', 12), width=10)
        ime1.grid(row=5, column=1)
        ime1.insert(0, self.ime_igralec1)

        ime2 = Entry(nov_game, font=('Times', 12), width=10)
        ime2.grid(row=5, column=3)
        ime2.insert(0, self.ime_igralec2)

        Button(nov_game, text="Prekliči", width=20, height=2,
                  command=lambda: new_game.destroy()).grid(row=6, column=0, columnspan=2, sticky=N+W+E+S)
        Button(nov_game, text="Zacni igro", width=20, height=2,
                  command=lambda: creategame()).grid(row=6, column=2, columnspan=2, sticky=N+W+E+S)

    def ponastavi(self):
        """pripravi polje za novo igro"""
        for i in self.id_polje:
            self.plosca.itemconfig(i, fill="")
        self.canvas1.delete(ALL)
        self.canvas2.delete(ALL)
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
            if self.na_potezi.barva == self.barva1:
                self.canvas1.itemconfig(self.play1ids[0], fill="")
                del(self.play1ids[0])
            else:
                self.canvas2.itemconfig(self.play2ids[0], fill="")
                del(self.play2ids[0])
            self.igra.poteza(prvopolje[0], prvopolje[1])
            if self.igra.mlin:
                self.DEFCON = 3
                self.textbox.set("Izberi zeton, ki ga bos pobral")
            else:
                self.zamenjaj_na_potezi()
        else:
            self.plosca.itemconfig(id_1, fill="")
            self.plosca.itemconfig(id_2, fill=self.na_potezi.barva)
            self.igra.poteza(drugopolje[0], drugopolje[1], prvopolje[0], prvopolje[1])
            if self.igra.mlin: #zahtevamo, da pobere žeton
                self.DEFCON = 3
                self.textbox.set("Izberi žeton, ki ga boš pobral!")
            else:
                #se pripravimo na naslednjo potezo
                self.DEFCON = 1
                self.zamenjaj_na_potezi()

    def izvedi_posebno_potezo(self,id_1,id_2=False):
        if id_1 != False:
            prvopolje = self.id_polje[id_1]
        if id_2 != False:
            drugopolje = self.id_polje[id_2]
        if id_2==False:
            self.plosca.itemconfig(id_1, fill=self.na_potezi.barva)
            self.igra.poteza(prvopolje[0], prvopolje[1])
            if self.na_potezi.barva == self.barva1:
                self.canvas1.itemconfig(self.play1ids[0], fill="")
                del(self.play1ids[0])
            else:
                self.canvas2.itemconfig(self.play2ids[0], fill="")
                del(self.play2ids[0])
        else:
            self.plosca.itemconfig(id_1, fill="")
            self.plosca.itemconfig(id_2, fill=self.na_potezi.barva)
            self.igra.poteza(drugopolje[0], drugopolje[1], prvopolje[0], prvopolje[1])

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
                    self.gui.DEFCON = 1
                    self.gui.plosca.itemconfig(self.prvi_klik, fill=self.gui.na_potezi.barva)
                    self.ponastavi()
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
        self.mislec = threading.Thread(target= lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))
        self.mislec.start()
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri ali je algoritem ze izracunal potezo"""
        if self.algoritem.poteza != None:
            if self.algoritem.poteza[2] == False:
                if self.algoritem.jemljem == (False,False):
                    id2 = self.gui.polje_id[(self.algoritem.poteza[0]),(self.algoritem.poteza[1])]
                    self.gui.izvedi_potezo(id2)
                else:
                    id2 = self.gui.polje_id[(self.algoritem.poteza[0]),(self.algoritem.poteza[1])]
                    id3 = self.gui.polje_id[(self.algoritem.jemljem[0]),(self.algoritem.jemljem[1])]
                    self.gui.izvedi_posebno_potezo(id2)  #ista k navadna sam da na koncu ne menja poteze
                    self.gui.vzami_zeton(id3)
            else:
                if self.algoritem.jemljem == (False,False):
                    id1 = self.gui.polje_id[(self.algoritem.poteza[2]),(self.algoritem.poteza[3])]
                    id2 = self.gui.polje_id[(self.algoritem.poteza[0]),(self.algoritem.poteza[1])]
                    self.gui.izvedi_potezo(id1,id2)
                else:
                    id1 = self.gui.polje_id[(self.algoritem.poteza[2]),(self.algoritem.poteza[3])]
                    id2 = self.gui.polje_id[(self.algoritem.poteza[0]),(self.algoritem.poteza[1])]
                    id3 = self.gui.polje_id[(self.algoritem.jemljem[0]),(self.algoritem.jemljem[1])]
                    self.gui.izvedi_posebno_potezo(id1,id2)
                    self.gui.vzami_zeton(id3)
            self.mislec = None
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

class Alpha_betta():
    """Vrne tri argumente (kam, od kje),(kaj jemljemo),vrednost poteze v obliki poteze"""
    def __init__(self,globina):
        self.globina = globina
        self.igra = None
        self.jaz = None
        self.poteza = None #sem algoritem shrani potezo ko jo naredi
        self.jemljem = None

    ZMAGA = 100000 # Mora biti vsaj 10^5
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def izracunaj_potezo(self,igra):
        self.igra = igra
        self.jaz = self.igra.na_potezi
        self.poteza = None
        self.jemljem = None
        (poteza, vrednost) = self.minimax(2, True)
        self.igra = None
        self.jaz= None
        self.poteza = poteza[:4]
        self.jemljem = poteza[4:]

    def vrednost_pozicije(self):
        """Vrne oceno vrednosti pozicije"""
        return self.igra.figurice[self.igra.na_potezi] - self.igra.figurice[nasprotnik(self.igra.na_potezi)]

    """
    def alpha_betta(self, globina, a, b, maksimiziramo):
        mozne = self.igra.veljavne_poteze()[:]
        random.shuffle(mozne)
        poteza = mozne[0]
        vrednost = 5
        if poteza[2] == False:
            if self.igra.postavljen_mlin((poteza[0], poteza[1]), True):
                jemljem = self.igra.veljavna_jemanja()[0]
            else:
                jemljem = None
        else:
            if self.igra.postavljen_mlin((poteza[0], poteza[1]), True, poteza[2], poteza[3]):
                jemljem = self.igra.veljavna_jemanja()[0]
            else:
                jemljem = None
        return (poteza, jemljem, vrednost)
    """

    def minimax(self, globina, maksimiziramo):
        (stanje, kdo) = self.igra.stanje
        if stanje == "ZMAGA":
            if kdo == self.jaz:
                return (None, Alpha_betta.ZMAGA)
            elif kdo == nasprotnik(self.jaz):
                return (None, - Alpha_betta.ZMAGA)
            else:
                pass
        elif stanje == "V TEKU":
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                if maksimiziramo:
                    najboljsa_poteza = None #(i,j,a,b,c,d)
                    vrednost_najboljse = - Alpha_betta.NESKONCNO
                    for p in self.igra.veljavne_poteze():
                        self.igra.poteza(p[0],p[1],p[2],p[3])
                        if self.igra.mlin == True:
                            for q in self.igra.veljavna_jemanja():
                                self.igra.odstrani_figurico(q[0],q[1])
                                vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                                self.igra.razveljavi_jemanje()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p + q #sestevanje tuplov
                            self.igra.mlin = False
                        else:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.razveljavi()
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p + (False,False,)
                else: #minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Alpha_betta.NESKONCNO
                    for p in self.igra.veljavne_poteze():
                        self.igra.poteza(p[0],p[1],p[2],p[3])
                        if self.igra.mlin == True:
                            for q in self.igra.veljavna_jemanja():
                                self.igra.odstrani_figurico(q[0],q[1])
                                vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                                self.igra.razveljavi_jemanje()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p + q
                            self.igra.mlin = False
                        else:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.razveljavi()
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p + (False,False)

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
                        
                                

if __name__ == "__main__":
    root = Tk()
    root.wm_title('Nine Men\'s Morris')
    root.resizable(width=FALSE, height=FALSE)
    okno = tkmlin(root)
    root.mainloop()
