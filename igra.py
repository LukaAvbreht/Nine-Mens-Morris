__author__ = 'LukaAvbreht, SamoKralj'
import logging

IGRALEC_BELI = "B"
IGRALEC_CRNI = "C"

def nasprotnik(igralec):
    """ Pove nasprotnega igralca. Koristno pri metodi poteza. """
    if igralec == IGRALEC_BELI:
        return IGRALEC_CRNI
    else:
        return IGRALEC_BELI


class Igra():
    """Program namenjen logiki in pravilom igre"""

    def __init__(self):  #remove nepotrebna polja
        self.plosca =[[None," "," ",None," "," ",None],
                      [" ",None," ",None," ",None," "],
                      [" "," ",None,None,None," "," "],
                      [None,None,None," ",None,None,None],
                      [" "," ",None,None,None," "," "],
                      [" ",None," ",None," ",None," "],
                      [None," "," ",None," "," ",None]]
        #None polja so prosta polja, " " so samo fillerji.
        self.na_potezi = IGRALEC_BELI
        self.zadnja_poteza = None  #to pomoje ne rabimo

        self.figurice = {IGRALEC_BELI: 0 , IGRALEC_CRNI: 0}
        #bi sproti spremljali koliko ima kdo figuric in v primeru, da je vrednost 2, 3 naredimo svoje
        #nam ni treba po vsaki potezi steti koliko ima kdo figuric

        self.faza = 0

        self.postavljenih = 0 #števec ki steje koliko figur je ze bilo postavljenih

        # self.faza = 0  --> Faza postavljanja figuric
        # self.faza = 1  --> Faza premikanja figuric
        
        self.zgodovina = []
        #Predlagam obliko: (pozicija, zadnja poteza, True - False, Pobrana figurica)
        #kjer True, False pove ali je bil vzpostavljen mlin in nato katera figurica je bil vzeta
        #bi po vsaki potezi belega in črnega shranili pozicijo?

        self.stanje = "Ni konec"
        #moznosti tega stanja so : ni konec, zmaga igralec beli, zmaga igralec crni, neodloceno

        self.sosedi = {(0,0) : [(0,3),(3,0)],
                  (0,3) : [(0,0),(0,6),(1,3)],
                  (0,6) : [(0,3),(3,6)],
                  (1,1) : [(1,3),(3,1)],
                  (1,3) : [(1,1),(1,5),(2,3),(0,3)],
                  (1,5) : [(1,3),(3,5)],
                  (2,2) : [(2,3),(3,2)],
                  (2,3) : [(2,2),(2,4),(1,3)],
                  (2,4) : [(2,3),(3,4)],
                  (3,0) : [(0,0),(6,0),(3,1)],
                  (3,1) : [(3,0),(3,2),(1,1),(5,1)],
                  (3,2) : [(3,1),(2,2),(4,2)],
                  (3,4) : [(2,4),(4,4),(3,5)],
                  (3,5) : [(3,4),(3,6),(1,5),(5,5)],
                  (3,6) : [(0,6),(6,6),(3,5)],
                  (4,2) : [(3,2),(4,3)],
                  (4,3) : [(4,2),(4,4),(5,3)],
                  (4,4) : [(4,3),(3,4)],
                  (5,1) : [(5,3),(3,1)],
                  (5,3) : [(5,1),(5,5),(4,3),(6,3)],
                  (5,5) : [(5,3),(3,5)],
                  (6,0) : [(3,0),(6,3)],
                  (6,3) : [(6,0),(6,6),(5,3)],
                  (6,6) : [(6,3),(3,6)],
                  }

    def izpisi_plosco(self):  #to je funkcija namenjena programerju
        """ Izpise trenutno ploščo na lep način. Vsako vrstico posebej."""
        for vrstica in self.plosca:
            print(vrstica)

    def je_veljavna(self, i, j, a = False, b = False):
        """Preveri, če je poteza veljavna.poteza na (i,j) iz (a,b)"""
        #################3### test za sosedi
        def test(slovar):
            for key in slovar.keys():
                for value in slovar[key]:
                    if key not in slovar[value]:
                        print(key, value)
                        return False
            return True
        #print(test(self.sosedi))
        ##################### test ni našel napake
        
        if self.faza == 0:
            return self.plosca[i][j] == None
        else:
            if self.plosca[i][j] == None and self.plosca[a][b] == self.na_potezi:
                return (i,j) in self.sosedi[(a,b)]
            else:
                return False

    def postavljen_mlin(self, poteza):
        """Glede na zadnjo potezo ugotovi ali je bil to potezo postavljen mlin. Vrne True ali False."""
        kombinacije = [
            #Vodoravne
            [(0,0),(0,3),(0,6)],
            [(6,0),(6,3),(6,6)],
            [(1,1),(1,3),(1,5)],
            [(5,1),(5,3),(5,5)],
            [(2,2),(2,3),(2,4)],
            [(4,2),(4,3),(4,4)],
            [(3,0),(3,1),(3,2)],
            [(3,4),(3,5),(3,6)],
            #Navpične
            [(0,0),(3,0),(6,0)],
            [(0,6),(3,6),(6,6)],
            [(1,1),(3,1),(5,1)],
            [(1,5),(3,5),(5,5)],
            [(2,2),(3,2),(4,2)],
            [(2,4),(3,4),(4,4)],
            [(0,3),(1,3),(2,3)],
            [(4,3),(5,3),(6,3)]]
        for trojka in kombinacije: #poteza oblike (i,j)
            if poteza in trojka:
                trojica = []
                for polje in trojka:
                    trojica.append(self.plosca[polje[0]][polje[1]])
                if trojica == [IGRALEC_BELI, IGRALEC_BELI, IGRALEC_BELI] or trojica == [IGRALEC_CRNI, IGRALEC_CRNI, IGRALEC_CRNI]:
                    return True
        return False

    def veljavne_poteze(self):
        """ Glede na trenutno fazo vrne mogoče možne poteze. """
        if self.faza == 0:  #trenba preverit ce si naredu mlin in smiselno dodati to v potezo
            mozne_poteze = []
            for i in range(7):
                for j in range(7):
                    if self.je_veljavna(i,j):
                        mozne_poteze.append((i,j))
            return mozne_poteze
        elif self.faza == 1:  #treba se dodat da preveri ce si naredu mlin
            mozne_poteze = []
            for i in range(7):
                for j in range(7):
                    if self.plosca[i][j] == self.na_potezi:
                        for sos in self.sosedi[(i,j)]:
                            if self.plosca[sos[0]][sos[1]] == None:
                                dod = (sos[0],sos[1],i,j)
                                mozne_poteze.append(dod)
            return mozne_poteze
        #faza premikanja figuric
        #odvisno od tega kdo je na potezi in koliko figuric še ima


    def lahko_jemljem(self, i, j):
        if self.plosca[i][j] == self.na_potezi:
            return self.postavljen_mlin((i, j)) == False
        else:
            return False

    # funkcijo poteza je treba popravit na nacin da dodava se dva argumenta ( se kateri kamen uzamemo, ce dosezemo mlin)
    # ki bo sta po defoltu enaka none
    def poteza(self, i, j, a=False, b=False):  #poteza od kod kam + nekaksen sistem da lahko postaviva nov kamen (za prvih 18 potez)
        """Izvede potezo. kam (i,j) od kje (a,b)"""
        if self.faza == 0:
            if self.je_veljavna(i,j):
                self.figurice[self.na_potezi] +=1
                self.postavljenih += 1
                if self.postavljenih >= 18: #V primeru, da je konec faze postavljanja
                    self.faza = 1
                self.plosca[i][j] = self.na_potezi
                self.zadnja_poteza = (i,j)
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                print("Poteza ni mogoča")
        else:
            if self.plosca[a][b] == self.na_potezi: #preveri da premikas svojo figurico
                if self.je_veljavna(i, j, a, b):  #preveri ali lahko tja premaknes svojo figurico (napisati je potrebno se da
                    # je mozno prestaviti figurico le na sosednja polja
                    self.plosca[a][b] = None
                    self.plosca[i][j] = self.na_potezi
                    self.na_potezi = nasprotnik(self.na_potezi)
                else:
                    print('Poteza iz ' + str((a,b)) + ' na polje ' + str((i,j)) + ' ni mogoča!' )
            else:
                print('tole pa ni tvoja figurica, Izberi svojo figuro')



    def odstrani_figurico(self, i, j):
        """Odstrani nasprotnikovo figurico v primeru da jo je veljavno odstraniti"""
        trenutni_nasprotnik = nasprotnik(self.na_potezi)
        if self.lahko_jemljem(i,j):
            self.plosca[i][j] = None
            self.figurice[trenutni_nasprotnik] -= 1

